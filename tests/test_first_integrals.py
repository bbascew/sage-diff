from sage.all import QQ, block_diagonal_matrix, matrix, var

from sage_diff.linear_systems import lie_derivative, linear_first_integrals


def assert_first_integrals(A, variables, expected_kinds):
    integrals = linear_first_integrals(A, variables)
    kinds = {integral.kind for integral in integrals}

    assert expected_kinds <= kinds
    for integral in integrals:
        assert lie_derivative(integral.expression, A, variables).simplify_full() == 0


def assert_first_integral_kinds(A, variables, expected_kinds):
    integrals = linear_first_integrals(A, variables)

    assert [integral.kind for integral in integrals] == expected_kinds
    for integral in integrals:
        assert lie_derivative(integral.expression, A, variables).simplify_full() == 0


def test_builds_real_spectral_integrals_from_paper_example_7():
    x = var("x1 x2 x3 x4", domain="real")
    A = matrix(
        QQ,
        [
            [1, -2, 0, -1],
            [-1, 4, -1, 2],
            [0, 2, 1, 1],
            [2, -4, 2, -2],
        ],
    )

    assert_first_integrals(A, x, {"real_zero", "real_ratio", "real_pair"})


def test_builds_zero_jordan_mixed_integral_from_paper_example_15():
    x = var("x1 x2 x3", domain="real")
    A = matrix(QQ, [[4, -5, 2], [5, -7, 3], [6, -9, 4]])

    assert_first_integrals(A, x, {"real_zero", "zero_jordan_real"})


def test_builds_long_real_jordan_chain_integrals_from_paper_example_20():
    x = var("x1 x2 x3 x4", domain="real")
    A = matrix(
        QQ,
        [
            [-5, -1, 4, 4],
            [2, 1, -4, 0],
            [-2, 0, 3, 1],
            [-5, -1, 2, 5],
        ],
    )

    assert_first_integrals(A, x, {"real_jordan_exponential", "real_jordan_psi_2", "real_jordan_psi_3"})


def test_builds_complex_and_complex_real_integrals():
    x = var("x1 x2 x3", domain="real")
    B = matrix(QQ, [[3, -1, 0], [1, 3, 0], [0, 0, 2]])
    A = B.transpose()

    assert_first_integrals(A, x, {"complex_eigen", "complex_real"})


def test_builds_complex_pair_integral():
    x = var("x1 x2 x3 x4", domain="real")
    B = matrix(QQ, [[0, -1, 0, 0], [1, 0, 0, 0], [0, 0, 0, -2], [0, 0, 2, 0]])
    A = B.transpose()

    assert_first_integrals(A, x, {"complex_eigen", "complex_pair"})


def test_builds_integrals_for_wikipedia_defective_jordan_example():
    x = var("x1 x2 x3 x4", domain="real")
    A = matrix(
        QQ,
        [
            [5, 4, 2, 1],
            [0, 1, -1, -1],
            [-1, -1, 3, 0],
            [1, 1, -1, 2],
        ],
    )

    assert_first_integrals(A, x, {"real_pair", "real_jordan_exponential"})


def test_builds_nilpotent_jordan_chain_integrals():
    x = var("x1 x2 x3 x4", domain="real")
    B = matrix(QQ, [[0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1], [0, 0, 0, 0]])
    A = B.transpose()

    assert_first_integrals(A, x, {"real_zero", "real_jordan_psi_2", "real_jordan_psi_3"})


def test_builds_integrals_for_sage_docs_mixed_jordan_blocks():
    x = var("x1 x2 x3 x4", domain="real")
    B = matrix(QQ, 4, [1, 0, 0, 0, 0, 1, 0, 0, 1, -1, 1, 0, 1, -1, 1, 2])
    A = B.transpose()

    assert_first_integrals(A, x, {"real_ratio", "real_pair", "real_jordan_exponential"})


def test_builds_integrals_for_complex_jordan_block():
    x = var("x1 x2 x3 x4", domain="real")
    B = matrix(QQ, [[2, -3, 1, 0], [3, 2, 0, 1], [0, 0, 2, -3], [0, 0, 3, 2]])
    A = B.transpose()

    integrals = linear_first_integrals(A, x)
    kinds = {integral.kind for integral in integrals}

    assert {"complex_eigen", "complex_jordan_exponential", "complex_jordan_angle"} <= kinds
    assert sum(integral.kind == "complex_jordan_angle" for integral in integrals) == 1
    for integral in integrals:
        assert lie_derivative(integral.expression, A, x).simplify_full() == 0


def test_builds_integrals_for_multiple_jordan_blocks_with_same_eigenvalue():
    x = var("x1 x2 x3 x4 x5", domain="real")
    block3 = matrix(QQ, [[2, 1, 0], [0, 2, 1], [0, 0, 2]])
    block2 = matrix(QQ, [[2, 1], [0, 2]])
    A = block_diagonal_matrix(block3, block2).transpose()

    assert_first_integral_kinds(
        A,
        x,
        ["real_ratio", "real_jordan_exponential", "real_jordan_psi_2", "real_jordan_exponential"],
    )


def test_builds_integrals_for_multiple_nilpotent_jordan_blocks():
    x = var("x1 x2 x3 x4 x5", domain="real")
    block3 = matrix(QQ, [[0, 1, 0], [0, 0, 1], [0, 0, 0]])
    block2 = matrix(QQ, [[0, 1], [0, 0]])
    A = block_diagonal_matrix(block3, block2).transpose()

    assert_first_integral_kinds(A, x, ["real_zero", "real_zero", "real_jordan_psi_2"])


def test_builds_zero_jordan_complex_mixed_integrals():
    x = var("x1 x2 x3 x4", domain="real")
    zero_block = matrix(QQ, [[0, 1], [0, 0]])
    complex_block = matrix(QQ, [[3, -2], [2, 3]])
    A = block_diagonal_matrix(zero_block, complex_block).transpose()

    assert_first_integral_kinds(
        A,
        x,
        ["real_zero", "complex_eigen", "zero_jordan_complex_radius", "zero_jordan_complex_angle"],
    )


def test_builds_integrals_for_complex_jordan_chain_of_length_three():
    x = var("x1 x2 x3 x4 x5 x6", domain="real")
    B = matrix(
        QQ,
        [
            [2, -3, 1, 0, 0, 0],
            [3, 2, 0, 1, 0, 0],
            [0, 0, 2, -3, 1, 0],
            [0, 0, 3, 2, 0, 1],
            [0, 0, 0, 0, 2, -3],
            [0, 0, 0, 0, 3, 2],
        ],
    )
    A = B.transpose()

    assert_first_integral_kinds(
        A,
        x,
        [
            "complex_eigen",
            "complex_jordan_exponential",
            "complex_jordan_angle",
            "complex_jordan_psi_2_real",
            "complex_jordan_psi_2_imaginary",
        ],
    )

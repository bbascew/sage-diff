from sage_diff.linear_systems.algebra import (
    as_matrix,
    has_positive_imaginary_part,
    is_real,
    is_zero,
    same_value,
    variables_for_system,
)
from sage_diff.linear_systems.formulas import (
    complex_eigen_integral,
    complex_pair_integral,
    complex_real_integral,
    jordan_chain_integrals,
    real_pair_integral,
    real_ratio_integral,
    real_zero_integral,
    zero_jordan_complex_integrals,
    zero_jordan_real_integral,
)
from sage_diff.linear_systems.spectrum import jordan_chains, spectral_vectors


def linear_first_integrals(A, variables=None):
    A = as_matrix(A)
    variables = variables_for_system(A.ncols(), variables)
    B = A.transpose()
    integrals = []
    spectral = spectral_vectors(B)
    real_entries = [(eigenvalue, vectors) for eigenvalue, vectors, _ in spectral if is_real(eigenvalue)]
    complex_entries = [
        (eigenvalue, vectors) for eigenvalue, vectors, _ in spectral if has_positive_imaginary_part(eigenvalue)
    ]

    integrals.extend(_real_single_eigenvalue_integrals(real_entries, variables))
    integrals.extend(_real_pair_integrals(real_entries, variables))
    integrals.extend(_complex_single_eigenvalue_integrals(complex_entries, variables))
    integrals.extend(_complex_real_integrals(complex_entries, real_entries, variables))
    integrals.extend(_complex_pair_integrals(complex_entries, variables))

    chains = jordan_chains(B)
    integrals.extend(_jordan_integrals(chains, variables))
    integrals.extend(_zero_jordan_mixed_integrals(chains, real_entries, complex_entries, variables))

    return unique_integrals(integrals)


def unique_integrals(integrals):
    seen = set()
    unique = []
    for integral in integrals:
        key = str(integral.expression.simplify_full())
        if key not in seen:
            seen.add(key)
            unique.append(integral)
    return unique


def _real_single_eigenvalue_integrals(real_entries, variables):
    integrals = []
    for eigenvalue, vectors in real_entries:
        if is_zero(eigenvalue):
            integrals.extend(real_zero_integral(v, variables) for v in vectors)
        if len(vectors) > 1 and not is_zero(eigenvalue):
            first = vectors[0]
            integrals.extend(real_ratio_integral(first, v, variables, eigenvalue) for v in vectors[1:])
    return integrals


def _real_pair_integrals(real_entries, variables):
    integrals = []
    for i, (lambda1, vectors1) in enumerate(real_entries):
        if is_zero(lambda1):
            continue
        for lambda2, vectors2 in real_entries[i + 1 :]:
            if is_zero(lambda2) or same_value(lambda1, lambda2):
                continue
            integrals.append(real_pair_integral(lambda1, vectors1[0], lambda2, vectors2[0], variables))
    return integrals


def _complex_single_eigenvalue_integrals(complex_entries, variables):
    return [complex_eigen_integral(eigenvalue, vectors[0], variables) for eigenvalue, vectors in complex_entries]


def _complex_real_integrals(complex_entries, real_entries, variables):
    integrals = []
    for complex_eigenvalue, complex_vectors in complex_entries:
        for real_eigenvalue, real_vectors in real_entries:
            if not is_zero(real_eigenvalue):
                integrals.append(
                    complex_real_integral(
                        complex_eigenvalue,
                        complex_vectors[0],
                        real_eigenvalue,
                        real_vectors[0],
                        variables,
                    )
                )
    return integrals


def _complex_pair_integrals(complex_entries, variables):
    integrals = []
    for i, (lambda1, vectors1) in enumerate(complex_entries):
        for lambda2, vectors2 in complex_entries[i + 1 :]:
            integrals.append(complex_pair_integral(lambda1, vectors1[0], lambda2, vectors2[0], variables))
    return integrals


def _jordan_integrals(chains, variables):
    integrals = []
    for eigenvalue, chain in chains:
        if len(chain) > 1 and (is_real(eigenvalue) or has_positive_imaginary_part(eigenvalue)):
            integrals.extend(jordan_chain_integrals(eigenvalue, chain, variables))
    return integrals


def _zero_jordan_mixed_integrals(chains, real_entries, complex_entries, variables):
    zero_chains = [chain for eigenvalue, chain in chains if len(chain) > 1 and is_zero(eigenvalue)]
    integrals = []
    for chain in zero_chains:
        for real_eigenvalue, real_vectors in real_entries:
            if not is_zero(real_eigenvalue):
                integrals.append(zero_jordan_real_integral(real_eigenvalue, real_vectors[0], chain, variables))
        for complex_eigenvalue, complex_vectors in complex_entries:
            integrals.extend(zero_jordan_complex_integrals(complex_eigenvalue, complex_vectors[0], chain, variables))
    return integrals

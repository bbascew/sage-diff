import sage_diff
import sage_diff.linear_systems as linear_systems


def test_package_exports_linear_system_helpers():
    for name in ["FirstIntegral", "lie_derivative", "linear_first_integrals", "linear_form"]:
        assert hasattr(sage_diff, name)


def test_linear_systems_exports_formula_helpers():
    for name in [
        "complex_eigen_integral",
        "complex_pair_integral",
        "complex_real_integral",
        "jordan_chain_integrals",
        "real_pair_integral",
        "real_ratio_integral",
        "real_zero_integral",
        "zero_jordan_complex_integrals",
        "zero_jordan_real_integral",
    ]:
        assert hasattr(linear_systems, name)

from sage.all import atan, exp

from sage_diff.linear_systems.algebra import complex_linear_parts, imaginary_part, linear_form, real_part
from sage_diff.linear_systems.models import FirstIntegral


def complex_eigen_integral(eigenvalue, eigenvector, variables):
    xi = real_part(eigenvalue)
    zeta = imaginary_part(eigenvalue)
    eta_form, mu_form = complex_linear_parts(eigenvector, variables)
    radius_squared = eta_form**2 + mu_form**2
    expression = (radius_squared * exp(-2 * xi / zeta * atan(mu_form / eta_form))).simplify_full()
    return FirstIntegral(
        expression,
        "complex_eigen",
        domain_conditions=(eta_form,),
        eigenvalues=(eigenvalue,),
        vectors=(tuple(eigenvector),),
    )


def complex_real_integral(complex_eigenvalue, complex_eigenvector, real_eigenvalue, real_eigenvector, variables):
    zeta = imaginary_part(complex_eigenvalue)
    eta_form, mu_form = complex_linear_parts(complex_eigenvector, variables)
    real_form = linear_form(real_eigenvector, variables)
    expression = (real_form * exp(-real_eigenvalue / zeta * atan(mu_form / eta_form))).simplify_full()
    return FirstIntegral(
        expression,
        "complex_real",
        domain_conditions=(eta_form,),
        eigenvalues=(complex_eigenvalue, real_eigenvalue),
        vectors=(tuple(complex_eigenvector), tuple(real_eigenvector)),
    )


def complex_pair_integral(lambda1, eigenvector1, lambda2, eigenvector2, variables):
    zeta1 = imaginary_part(lambda1)
    zeta2 = imaginary_part(lambda2)
    eta1_form, mu1_form = complex_linear_parts(eigenvector1, variables)
    eta2_form, mu2_form = complex_linear_parts(eigenvector2, variables)
    expression = (zeta1 * atan(mu2_form / eta2_form) - zeta2 * atan(mu1_form / eta1_form)).simplify_full()
    return FirstIntegral(
        expression,
        "complex_pair",
        domain_conditions=(eta1_form, eta2_form),
        eigenvalues=(lambda1, lambda2),
        vectors=(tuple(eigenvector1), tuple(eigenvector2)),
    )

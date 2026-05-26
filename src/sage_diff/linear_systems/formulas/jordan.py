from sage.all import atan, binomial, exp

from sage_diff.linear_systems.algebra import (
    complex_linear_parts,
    expression_imaginary_part,
    expression_real_part,
    imaginary_part,
    is_real,
    is_zero,
    linear_form,
    real_part,
)
from sage_diff.linear_systems.models import FirstIntegral


def jordan_chain_integrals(eigenvalue, chain, variables):
    if is_real(eigenvalue):
        return real_jordan_chain_integrals(eigenvalue, chain, variables)
    return complex_jordan_chain_integrals(eigenvalue, chain, variables)


def zero_jordan_real_integral(real_eigenvalue, real_eigenvector, zero_chain, variables):
    base_form = linear_form(zero_chain[0], variables)
    associated_form = linear_form(zero_chain[1], variables)
    real_form = linear_form(real_eigenvector, variables)
    expression = (real_form * exp(-real_eigenvalue * associated_form / base_form)).simplify_full()
    return FirstIntegral(
        expression,
        "zero_jordan_real",
        domain_conditions=(base_form,),
        eigenvalues=(0, real_eigenvalue),
        vectors=(tuple(zero_chain[0]), tuple(zero_chain[1]), tuple(real_eigenvector)),
    )


def zero_jordan_complex_integrals(complex_eigenvalue, complex_eigenvector, zero_chain, variables):
    xi = real_part(complex_eigenvalue)
    zeta = imaginary_part(complex_eigenvalue)
    base_form = linear_form(zero_chain[0], variables)
    associated_form = linear_form(zero_chain[1], variables)
    eta_form, mu_form = complex_linear_parts(complex_eigenvector, variables)
    radius_squared = eta_form**2 + mu_form**2
    first = (radius_squared * exp(-2 * xi * associated_form / base_form)).simplify_full()
    second = (atan(mu_form / eta_form) - zeta * associated_form / base_form).simplify_full()
    return [
        FirstIntegral(
            first,
            "zero_jordan_complex_radius",
            domain_conditions=(base_form,),
            eigenvalues=(0, complex_eigenvalue),
            vectors=(tuple(zero_chain[0]), tuple(zero_chain[1]), tuple(complex_eigenvector)),
        ),
        FirstIntegral(
            second,
            "zero_jordan_complex_angle",
            domain_conditions=(base_form, eta_form),
            eigenvalues=(0, complex_eigenvalue),
            vectors=(tuple(zero_chain[0]), tuple(zero_chain[1]), tuple(complex_eigenvector)),
        ),
    ]


def real_jordan_chain_integrals(eigenvalue, chain, variables):
    forms = [linear_form(chain_vector, variables) for chain_vector in chain]
    integrals = []

    if not is_zero(eigenvalue):
        expression = (forms[0] * exp(-eigenvalue * forms[1] / forms[0])).simplify_full()
        integrals.append(
            FirstIntegral(
                expression,
                "real_jordan_exponential",
                domain_conditions=(forms[0],),
                eigenvalues=(eigenvalue,),
                vectors=tuple(tuple(chain_vector) for chain_vector in chain[:2]),
            )
        )

    for index, psi in enumerate(chain_psi(forms)[1:], start=2):
        integrals.append(
            FirstIntegral(
                psi.simplify_full(),
                f"real_jordan_psi_{index}",
                domain_conditions=(forms[0],),
                eigenvalues=(eigenvalue,),
                vectors=tuple(tuple(chain_vector) for chain_vector in chain[: index + 1]),
            )
        )

    return integrals


def complex_jordan_chain_integrals(eigenvalue, chain, variables):
    xi = real_part(eigenvalue)
    zeta = imaginary_part(eigenvalue)
    eta0, mu0 = complex_linear_parts(chain[0], variables)
    eta1, mu1 = complex_linear_parts(chain[1], variables)
    radius_squared = eta0**2 + mu0**2
    dot = eta0 * eta1 + mu0 * mu1
    cross = eta0 * mu1 - mu0 * eta1
    first = (radius_squared * exp(-2 * (xi * dot - zeta * cross) / radius_squared)).simplify_full()
    second = (atan(mu0 / eta0) - (zeta * dot + xi * cross) / radius_squared).simplify_full()
    integrals = [
        FirstIntegral(
            first,
            "complex_jordan_exponential",
            domain_conditions=(radius_squared,),
            eigenvalues=(eigenvalue,),
            vectors=tuple(tuple(chain_vector) for chain_vector in chain[:2]),
        ),
        FirstIntegral(
            second,
            "complex_jordan_angle",
            domain_conditions=(eta0,),
            eigenvalues=(eigenvalue,),
            vectors=tuple(tuple(chain_vector) for chain_vector in chain[:2]),
        ),
    ]
    forms = [linear_form(chain_vector, variables) for chain_vector in chain]
    base_form = forms[0]

    for index, psi in enumerate(chain_psi(forms)[1:], start=2):
        integrals.append(
            FirstIntegral(
                expression_real_part(psi).simplify_full(),
                f"complex_jordan_psi_{index}_real",
                domain_conditions=(base_form,),
                eigenvalues=(eigenvalue,),
                vectors=tuple(tuple(chain_vector) for chain_vector in chain[: index + 1]),
            )
        )
        integrals.append(
            FirstIntegral(
                expression_imaginary_part(psi).simplify_full(),
                f"complex_jordan_psi_{index}_imaginary",
                domain_conditions=(base_form,),
                eigenvalues=(eigenvalue,),
                vectors=tuple(tuple(chain_vector) for chain_vector in chain[: index + 1]),
            )
        )

    return integrals


def chain_psi(forms):
    values = []
    for k in range(1, len(forms)):
        value = forms[k]
        for i in range(1, k):
            value -= binomial(k - 1, i - 1) * values[i - 1] * forms[k - i]
        values.append((value / forms[0]).simplify_full())
    return values

from sage_diff.linear_systems.algebra import linear_form
from sage_diff.linear_systems.models import FirstIntegral


def real_zero_integral(eigenvector, variables):
    expression = linear_form(eigenvector, variables).simplify_full()
    return FirstIntegral(expression, "real_zero", eigenvalues=(0,), vectors=(tuple(eigenvector),))


def real_ratio_integral(eigenvector1, eigenvector2, variables, eigenvalue=None):
    denominator = linear_form(eigenvector1, variables)
    numerator = linear_form(eigenvector2, variables)
    expression = (numerator / denominator).simplify_full()
    eigenvalues = () if eigenvalue is None else (eigenvalue,)
    return FirstIntegral(
        expression,
        "real_ratio",
        domain_conditions=(denominator,),
        eigenvalues=eigenvalues,
        vectors=(tuple(eigenvector1), tuple(eigenvector2)),
    )


def real_pair_integral(lambda1, eigenvector1, lambda2, eigenvector2, variables):
    form1 = linear_form(eigenvector1, variables)
    form2 = linear_form(eigenvector2, variables)
    expression = (form1**lambda2 * form2 ** (-lambda1)).simplify_full()
    return FirstIntegral(
        expression,
        "real_pair",
        domain_conditions=(form1, form2),
        eigenvalues=(lambda1, lambda2),
        vectors=(tuple(eigenvector1), tuple(eigenvector2)),
    )

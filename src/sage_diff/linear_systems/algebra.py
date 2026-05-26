from sage.all import matrix, var, vector


def lie_derivative(expression, A, variables):
    A = as_matrix(A)
    variables = tuple(variables)
    field_values = A * vector(variables)
    return sum(expression.diff(variable) * field_values[i] for i, variable in enumerate(variables)).simplify_full()


def linear_form(coefficients, variables):
    coefficients = tuple(coefficients)
    variables = tuple(variables)
    return sum(coefficients[i] * variables[i] for i in range(len(variables)))


def as_matrix(A):
    if hasattr(A, "nrows") and hasattr(A, "ncols"):
        return A
    return matrix(A)


def variables_for_system(size, variables):
    if variables is not None:
        return tuple(variables)
    created = var(" ".join(f"x{i + 1}" for i in range(size)), domain="real")
    if size == 1:
        return (created,)
    return tuple(created)


def complex_linear_parts(eigenvector, variables):
    real_coefficients = [real_part(coefficient) for coefficient in eigenvector]
    imaginary_coefficients = [imaginary_part(coefficient) for coefficient in eigenvector]
    return linear_form(real_coefficients, variables), linear_form(imaginary_coefficients, variables)


def real_part(value):
    if hasattr(value, "real_part"):
        return value.real_part()
    if hasattr(value, "real"):
        return value.real()
    return value


def imaginary_part(value):
    if hasattr(value, "imag_part"):
        return value.imag_part()
    if hasattr(value, "imag"):
        return value.imag()
    return 0


def expression_real_part(expression):
    if hasattr(expression, "real_part"):
        return expression.real_part()
    return expression.real()


def expression_imaginary_part(expression):
    if hasattr(expression, "imag_part"):
        return expression.imag_part()
    return expression.imag()


def is_real(value):
    return is_zero(imaginary_part(value))


def is_zero(value):
    try:
        return bool(value == 0 or value.simplify_full() == 0)
    except Exception:
        return bool(value == 0)


def same_value(left, right):
    return is_zero(left - right)


def has_positive_imaginary_part(value):
    imaginary = imaginary_part(value)
    if is_zero(imaginary):
        return False
    try:
        return bool(imaginary > 0)
    except Exception:
        return imaginary.n() > 0

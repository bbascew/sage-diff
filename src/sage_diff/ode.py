from sage.all import desolve, diff


def derivative(function_expression, variable, order: int = 1):
    return diff(function_expression, variable, order)


def solve_ode(equation, function_expression, **kwargs):
    return desolve(equation, function_expression, **kwargs)

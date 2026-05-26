from sage_diff import create_function, derivative, solve_ode, symbol


def test_solves_first_order_linear_ode():
    x = symbol("x")
    y = create_function("y", x)

    solution = solve_ode(derivative(y, x) - y, y)

    assert (derivative(solution, x) - solution).simplify_full() == 0

from sage.all import function, var


def symbol(name: str):
    return var(name)


def create_function(name: str, variable):
    return function(name)(variable)


def simplify(expression):
    return expression.simplify_full()

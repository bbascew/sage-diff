from sage.all import SR, factorial

from sage_diff.linear_systems.algebra import is_zero, same_value


def spectral_vectors(B):
    try:
        return B.eigenvectors_right()
    except Exception:
        return B.change_ring(SR).eigenvectors_right()


def jordan_chains(B):
    try:
        J, P = B.change_ring(SR).jordan_form(transformation=True)
    except Exception:
        return []

    chains = []
    index = 0
    size = J.nrows()
    while index < size:
        eigenvalue = J[index, index]
        length = 1
        while (
            index + length < size
            and same_value(J[index + length, index + length], eigenvalue)
            and not is_zero(J[index + length - 1, index + length])
        ):
            length += 1
        chain = [factorial(k) * P.column(index + k) for k in range(length)]
        chains.append((eigenvalue, chain))
        index += length
    return chains

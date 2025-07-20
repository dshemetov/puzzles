from bisect import insort
from collections.abc import Iterable
from functools import partial
from itertools import accumulate


def apply_until_fixed(func):
    """Repeatedly compose a function until the output does not change.

    Assumes func has a single non-keyword argument.
    """

    def new_func(*args, **kwargs):
        new_val, old_val = func(*args, **kwargs), object()
        while new_val != old_val:
            new_val, old_val = func(new_val, **kwargs), new_val
        return new_val

    return new_func


def apply_until_fixed_list(func):
    """Repeatedly compose a function until the output does not change; return the list of intermediate values.

    Assumes func has a single non-keyword argument.
    """

    def new_func(*args, **kwargs):
        new_val, old_val = func(*args, **kwargs), object()
        vals = [new_val]
        while new_val != old_val:
            new_val, old_val = func(new_val, **kwargs), new_val
            vals.append(new_val)
        return new_val, vals

    return new_func


def until_fixed(it: Iterable) -> Iterable:
    return accumulate(it, no_repeat)


def no_repeat(prev, curr):
    if prev == curr:
        raise StopIteration
    return curr


def until_close(it: Iterable, tol: float = 0.001) -> Iterable:
    return accumulate(it, partial(within_tolerance, tol))


def within_tolerance(tol: float, prev: float, curr: float) -> float:
    if abs(prev - curr) < tol:
        raise StopIteration
    return curr


def binary_to_int(ls: list[int]) -> int:
    """Convert a list of 0's and 1's to an integer.

    Examples:
    >>> binary_to_int([1, 0, 1])
    5
    """
    return int("".join(str(i) for i in ls), 2)


def reverse_dict(d: dict) -> dict:
    """This thing better be a bijection.

    Examples:
    >>> reverse_dict({"a": 2, "b": 3})
    {2: 'a', 3: 'b'}
    """
    return {value: key for key, value in d.items()}


def get_gcd(a: int, b: int) -> int:
    """Euclidean algorithm greatest common divisor.

    Returns the largest integer d such that d | a and d | b.

    Examples:
    >>> get_gcd(6, 4)
    2
    >>> get_gcd(4, 6)
    2
    >>> get_gcd(5, 17)
    1
    """
    r, r_ = a, b
    while r_ > 0:
        r, r_ = r_, r % r_
    return r


def get_bezout_coefficients(a: int, b: int) -> tuple[int, int]:
    """Extended Euclidean algorithm.

    Returns integer coefficients x and y such that x * a + y * b = gcd(a, b).

    Examples:
    >>> get_bezout_coefficients(6, 4)
    (1, -1)
    >>> get_bezout_coefficients(4, 6)
    (-1, 1)
    >>> get_bezout_coefficients(5, 17)
    (7, -2)
    """
    s, s_ = 0, 1
    t, t_ = 1, 0
    r, r_ = a, b
    while r_ > 0:
        q = r // r_
        r, r_ = r_, r - q * r_
        s, s_ = s_, s - q * s_
        t, t_ = t_, t - q * t_
    return (t, s)


def nlargest(n: int, it: Iterable) -> list:
    """
    Examples:
    >>> nlargest(5, [5, 4, 3, 10, 2, 5])
    [3, 4, 5, 5, 10]
    """
    top_n = []
    for e in it:
        insort(top_n, e)
        if len(top_n) > n:
            top_n.pop(0)
    return top_n

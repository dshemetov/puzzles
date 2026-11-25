from bisect import bisect_left


def guess(num: int) -> int:
    __pick__ = 6
    if num == __pick__:
        return 0
    if num > __pick__:
        return -1
    return 1


def p374b(n: int) -> int:
    """Examples
    >>> p374b(10)
    6

    """
    return bisect_left(range(0, n), 0, lo=0, hi=n, key=lambda x: -guess(x))

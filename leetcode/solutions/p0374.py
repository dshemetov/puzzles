def guess(num: int) -> int:
    __pick__ = 6
    if num == __pick__:
        return 0
    if num > __pick__:
        return -1
    return 1


def p374(n: int) -> int:
    """374. Guess Number Higher or Lower https://leetcode.com/problems/guess-number-higher-or-lower/

    Lessons learned:
    - bisect_left has a 'key' argument as of 3.10.

    Examples
    --------
    >>> p374(10)
    6

    """
    lo, hi = 1, n
    while lo < hi:
        mid = (lo + hi) // 2
        out = guess(mid)
        if out == 1:
            lo = mid + 1
        elif out == -1:
            hi = mid - 1
        else:
            return mid

    return lo

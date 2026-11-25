import math


def p1680(n: int) -> int:
    """1680. Concatenation of Consecutive Binary Numbers https://leetcode.com/problems/concatenation-of-consecutive-binary-numbers/

    Examples
    --------
    >>> p1680(1)
    1
    >>> p1680(3)
    27
    >>> p1680(12)
    505379714

    """
    M = 10**9 + 7
    total = 1
    for i in range(2, n + 1):
        total = ((total << math.floor(math.log2(i)) + 1) + i) % M

    return total

import math


def p1323(num: int) -> int:
    """1323. Maximum 69 Number https://leetcode.com/problems/maximum-69-number/

    Lessons learned:
    - Converting to a string and using replace is surprisingly fast.
    - Just need to accept that Python string built-ins are in C-land.

    Examples
    --------
    >>> p1323(9669)
    9969
    >>> p1323(9996)
    9999
    >>> p1323(9999)
    9999

    """
    for i in range(math.floor(math.log10(num)) + 1, -1, -1):
        if num // 10**i % 10 == 6:
            return num + 3 * 10**i
    return num

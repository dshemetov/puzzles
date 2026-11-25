import math


def p9(x: int) -> bool:
    """9. Palindrome Number https://leetcode.com/problems/palindrome-number/

    Examples
    --------
    >>> p9(121)
    True
    >>> p9(-121)
    False
    >>> p9(10)
    False
    >>> p9(0)
    True
    >>> p9(1)
    True
    >>> p9(1331)
    True
    >>> p9(1332)
    False
    >>> p9(133454331)
    True
    >>> p9(1122)
    False

    """
    if x < 0:
        return False
    if x == 0:
        return True

    num_digits = math.floor(math.log10(x)) + 1

    if num_digits == 1:
        return True

    return all(x // 10**i % 10 == x // 10 ** (num_digits - i - 1) % 10 for i in range(num_digits // 2))

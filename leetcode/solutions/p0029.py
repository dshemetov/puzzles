def p29(dividend: int, divisor: int) -> int:
    """29. Divide Two Integers https://leetcode.com/problems/divide-two-integers

    The straightforward approach is to just subtract divisor from dividend until
    dividend is less than divisor. This is O(n) (where n = dividend/divisor) and
    will not work for large numbers. We can speed this up by doubling the
    divisor after each subtraction and resetting once dividend is smaller than
    the doubled value. This algorithm is O(log(n)).

    Examples
    --------
    >>> p29(10, 3)
    3
    >>> p29(7, -3)
    -2
    >>> p29(0, 1)
    0
    >>> p29(1, 1)
    1

    """
    sign = 1 if dividend * divisor > 0 else -1
    dividend, divisor = abs(dividend), abs(divisor)
    quotient = 0

    while dividend >= divisor:
        temp, i = divisor, 1
        while dividend >= temp:
            dividend -= temp
            quotient += i
            i <<= 1
            temp <<= 1

    return min(2**31 - 1, max(-(2**31), sign * quotient))

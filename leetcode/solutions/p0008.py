def p8(s: str) -> int:
    """8. String to Integer (atoi) https://leetcode.com/problems/string-to-integer-atoi/

    Examples
    --------
    >>> p8("42")
    42
    >>> p8("   -42")
    -42
    >>> p8("4193 with words")
    4193
    >>> p8("words and 987")
    0
    >>> p8("-91283472332")
    -2147483648
    >>> p8("91283472332")
    2147483647
    >>> p8("3.14159")
    3
    >>> p8("+-2")
    0
    >>> p8("  -0012a42")
    -12
    >>> p8("  +0 123")
    0
    >>> p8("-0")
    0

    """
    _max = 2**31 - 1
    _min = 2**31

    factor = 0
    num = 0
    digits_started = False
    for c in s:
        if not digits_started:
            if c == " ":
                continue
            if c == "-":
                factor = -1
                digits_started = True
            elif c == "+":
                factor = 1
                digits_started = True
            elif c.isdigit():
                factor = 1
                digits_started = True
                num = int(c)
            else:
                return 0
        elif c.isdigit():
            num = num * 10 + int(c)
            if factor == 1 and num > _max:
                return _max
            if factor == -1 and num > _min:
                return -_min
        else:
            break

    return factor * num

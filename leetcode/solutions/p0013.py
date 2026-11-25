def p13(s: str) -> int:
    """13. Roman to Integer https://leetcode.com/problems/roman-to-integer/

    Examples
    --------
    >>> p13("III")
    3
    >>> p13("IV")
    4
    >>> p13("IX")
    9
    >>> p13("LVIII")
    58
    >>> p13("MCMXCIV")
    1994

    """
    d = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100, "D": 500, "M": 1000}

    total = 0
    for i in range(len(s) - 1):
        if d[s[i]] < d[s[i + 1]]:
            total -= d[s[i]]
        else:
            total += d[s[i]]

    return total + d[s[i + 1]]

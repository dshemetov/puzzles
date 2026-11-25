def get_fibonacci_number(n: int) -> int:
    """Return the nth Fibonacci number, where F(0) = 0 and F(1) = 1.

    Examples
    --------
    >>> [get_fibonacci_number(i) for i in range(10)]
    [0, 1, 1, 2, 3, 5, 8, 13, 21, 34]

    """
    phi = (1 + 5**0.5) / 2
    return int(phi**n / 5**0.5 + 0.5)


def p91(s: str) -> int:
    """91. Decode Ways https://leetcode.com/problems/decode-ways/

    Lessons learned:
    - My first observation was that characters in "34567890" acted as separators,
    where I could split the string into substrings that could be decoded
    independently. My second observation was that the number of ways to decode a
    string of nothing but "1" and "2" characters was the Fibonacci number
    F(n+1), where n is the number of characters in the string. Combining these
    two speedups with recursion gave me the first solution, which had middle of
    the pack runtime and memory usage.
    - The second solution is a very clean dynamic programming approach I lifted
    from the discussion section. Define

        dp(i) = number of ways to decode the substring s[:i]

    The recurrence relation is

        dp(i) = dp(i-1) + dp(i-2) if "11" <= s[i-2:i] <= "26" and s[i-2:i] != "20"
                = dp(i-1) if s[i-1] != "0" and s[i-2:i] > "26"
                = dp(i-2) if "10" == s[i-2:i] or "20" == s[i-2:i]
                = 0 otherwise
        dp(0) = 1
        dp(1) = 1 if s[0] != "0" else 0

    - Fun fact: the number of binary strings of length n with no consecutive zeros
    corresponds to the Fibonacci number F(n+2). This diagram helps visualize the
    recursion:
    https://en.wikipedia.org/wiki/Composition_(combinatorics)#/media/File:Fibonacci_climbing_stairs.svg.

    Examples
    --------
    >>> p91("0")
    0
    >>> p91("06")
    0
    >>> p91("1")
    1
    >>> p91("12")
    2
    >>> p91("111")
    3
    >>> p91("35")
    1
    >>> p91("226")
    3
    >>> p91("2020")
    1
    >>> p91("2021")
    2
    >>> p91("2022322")
    6

    """
    valid_codes = {str(x) for x in range(1, 27)}

    def recurse(s1: str) -> int:
        if s1[0] == "0":
            return 0

        if len(s1) == 1:
            return 1

        if len(s1) == 2:
            if int(s1) <= 26 and s1[1] != "0":
                return 2
            if int(s1) <= 26 and s1[1] == "0":
                return 1
            if int(s1) > 26 and s1[1] != "0":
                return 1
            return 0

        if set(s1) <= {"1", "2"}:
            return get_fibonacci_number(len(s1) + 1)

        if s1[:2] in valid_codes:
            return recurse(s1[1:]) + recurse(s1[2:])

        return recurse(s1[1:])

    total = 1
    prev = 0
    for i, c in enumerate(s):
        if c in "34567890":
            total *= recurse(s[prev : i + 1])
            prev = i + 1

    if s[prev:]:
        total *= recurse(s[prev:])

    return total

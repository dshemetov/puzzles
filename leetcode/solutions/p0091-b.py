def p91b(s: str) -> int:
    """Examples
    >>> p91b("0")
    0
    >>> p91b("06")
    0
    >>> p91b("1")
    1
    >>> p91b("12")
    2
    >>> p91b("111")
    3
    >>> p91b("35")
    1
    >>> p91b("226")
    3
    >>> p91b("2020")
    1
    >>> p91b("2021")
    2
    >>> p91b("2022322")
    6

    """
    if not s or s[0] == "0":
        return 0

    dp = [0] * (len(s) + 1)
    dp[0:2] = [1, 1]

    for i in range(2, len(s) + 1):
        if "11" <= s[i - 2 : i] <= "19" or "21" <= s[i - 2 : i] <= "26":
            dp[i] = dp[i - 1] + dp[i - 2]
        elif s[i - 1] != "0":
            dp[i] = dp[i - 1]
        elif s[i - 2 : i] == "10" or s[i - 2 : i] == "20":
            dp[i] = dp[i - 2]

    return dp[-1]

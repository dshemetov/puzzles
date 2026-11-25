def p32(s: str) -> int:
    """32. Longest Valid Parentheses https://leetcode.com/problems/longest-valid-parentheses/

    Example:
    >>> p32("(()")
    2
    >>> p32(")()())")
    4
    >>> p32("")
    0
    >>> p32("()")
    2
    """
    if not s:
        return 0

    nums = [int(c.replace("(", "1").replace(")", "-1")) for c in s]
    n = len(nums)
    prefix = [0] * (n + 1)
    for i in range(1, n + 1):
        prefix[i] = prefix[i - 1] + nums[i - 1]

    # print(prefix)
    result = 0
    ms = [(0, 0)]
    for i in range(1, n + 1):
        # print(ms)
        if not ms:
            ms.append((i, prefix[i]))
            continue

        if prefix[i] < ms[-1][1]:
            ms.pop()
            if ms and prefix[i] == ms[-1][1]:
                result = max(result, i - ms[-1][0])
            else:
                ms.append((i, prefix[i]))

        elif prefix[i] > ms[-1][1]:
            ms.append((i, prefix[i]))

    return result

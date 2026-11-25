def p1544(s: str) -> str:
    """1544. Make The String Great https://leetcode.com/problems/make-the-string-great/

    Examples
    --------
    >>> p1544("leEeetcode")
    'leetcode'
    >>> p1544("abBAcC")
    ''
    >>> p1544("s")
    's'

    """
    stack = []
    for c in s:
        if stack and stack[-1].lower() == c.lower() and stack[-1] != c:
            stack.pop()
        else:
            stack.append(c)
    return "".join(stack)

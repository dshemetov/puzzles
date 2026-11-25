def p1047(s: str) -> str:
    """1047. Remove All Adjacent Duplicates in String https://leetcode.com/problems/remove-all-adjacent-duplicates-in-string/

    Examples
    --------
    >>> p1047("abbaca")
    'ca'
    >>> p1047("aaaaaaaa")
    ''

    """
    stack = []
    for c in s:
        if stack and c == stack[-1]:
            stack.pop()
        else:
            stack.append(c)
    return "".join(stack)

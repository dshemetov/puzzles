from collections import deque


def p20(s: str) -> bool:
    """20. Valid Parentheses https://leetcode.com/problems/valid-parentheses/

    Examples
    --------
    >>> p20("()")
    True
    >>> p20("()[]{}")
    True
    >>> p20("(]")
    False

    """
    stack = deque()
    bracket_map = {"(": ")", "[": "]", "{": "}"}
    for c in s:
        if c in bracket_map:
            stack.append(c)
        elif not stack or bracket_map[stack.pop()] != c:
            return False

    return not stack

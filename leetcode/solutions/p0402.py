def p402(num: str, k: int) -> str:
    """402. Remove k Digits https://leetcode.com/problems/remove-k-digits/

    Lessons learned:
    - try to build up a heuristic algorithm from a few examples

    Examples
    --------
    >>> p402("1432219", 3)
    '1219'
    >>> p402("10200", 1)
    '200'
    >>> p402("10", 2)
    '0'
    >>> p402("9", 1)
    '0'
    >>> p402("112", 1)
    '11'

    """
    if len(num) <= k:
        return "0"

    stack = []
    for c in num:
        if c == "0" and not stack:
            continue
        while stack and stack[-1] > c and k > 0:
            stack.pop()
            k -= 1
        stack.append(c)

    if k > 0:
        stack = stack[:-k]

    return "".join(stack).lstrip("0") or "0"

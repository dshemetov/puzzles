def p22(n: int) -> list[str]:
    """22. Generate Parentheses https://leetcode.com/problems/generate-parentheses/

    Examples
    --------
    >>> p22(3)
    ['((()))', '(()())', '(())()', '()(())', '()()()']
    >>> p22(1)
    ['()']

    """
    if n == 1:
        return ["()"]

    res: list[str] = [""]
    for _ in range(2 * n):
        temp = []
        for x in res:
            if x.count("(") < n:
                temp.append(x + "(")
            if x.count("(") > x.count(")"):
                temp.append(x + ")")
        res = temp

    return res

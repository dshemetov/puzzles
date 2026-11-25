def p791(order: str, s: str) -> str:
    """791. Custom Sort String https://leetcode.com/problems/custom-sort-string/

    Examples
    --------
    >>> p791("cba", "abcd")
    'cbad'
    >>> p791("cba", "abc")
    'cba'
    >>> p791("bcafg", "abcd")
    'bcad'

    """

    def key_fn(t: str) -> int:
        try:
            return order.index(t)
        except ValueError:
            return 30

    return "".join(sorted(s, key=key_fn))

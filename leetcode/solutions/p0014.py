def p14(strs: list[str]) -> str:
    """14. Longest Common Prefix https://leetcode.com/problems/longest-common-prefix/

    Examples
    --------
    >>> p14(["flower", "flow", "flight"])
    'fl'
    >>> p14(["dog", "racecar", "car"])
    ''
    >>> p14(["dog", "dog", "dog", "dog"])
    'dog'

    """
    prefix = strs[0]
    for s in strs[1:]:
        while not s.startswith(prefix):
            prefix = prefix[:-1]
        if prefix == "":
            break
    return prefix

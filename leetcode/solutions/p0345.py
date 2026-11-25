def p345(s: str) -> str:
    """345. Reverse Vowels of a String https://leetcode.com/problems/reverse-vowels-of-a-string/

    Examples
    --------
    >>> p345("hello")
    'holle'
    >>> p345("leetcode")
    'leotcede'

    """
    if len(s) == 1:
        return s

    hi = len(s) - 1
    s_ = []
    for c in s:
        if c in "aeiouAEIOU":
            while s[hi] not in "aeiouAEIOU":
                hi -= 1
            s_.append(s[hi])
            hi -= 1
        else:
            s_.append(c)

    return "".join(s_)

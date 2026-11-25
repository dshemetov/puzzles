def p3(s: str) -> int:
    """3. Longest Substring Without Repeating Characters https://leetcode.com/problems/longest-substring-without-repeating-characters/

    Examples
    --------
    >>> p3("a")
    1
    >>> p3("aa")
    1
    >>> p3("aaa")
    1
    >>> p3("aab")
    2
    >>> p3("abba")
    2
    >>> p3("abccba")
    3
    >>> p3("au")
    2
    >>> p3("cdd")
    2
    >>> p3("abcabcbb")
    3
    >>> p3("aabcdef")
    6
    >>> p3("abcdeffff")
    6
    >>> p3("dvdf")
    3
    >>> p3("ohomm")
    3

    """
    if not s:
        return 0

    longest = 1
    lo = 0
    hi = 1
    char_set = set(s[lo])
    while hi < len(s):
        if s[hi] not in char_set:
            char_set.add(s[hi])
            hi += 1
            longest = max(longest, hi - lo)
        else:
            char_set.remove(s[lo])
            lo += 1

    return longest

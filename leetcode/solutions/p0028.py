def p28(haystack: str, needle: str) -> int:
    """28. Find the Index of the First Occurrence in a String https://leetcode.com/problems/find-the-index-of-the-first-occurrence-in-a-string

    Examples
    --------
    >>> p28("sadbutsad", "sad")
    0
    >>> p28("sadbutsad", "but")
    3
    >>> p28("leetcode", "leeto")
    -1

    """
    if needle in haystack:
        return haystack.index(needle)
    return -1

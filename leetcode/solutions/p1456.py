def p1456(s: str, k: int) -> int:
    """1456. Maximum Number of Vowels in a Substring of Given Length https://leetcode.com/problems/maximum-number-of-vowels-in-a-substring-of-given-length/

    Lessons learned:
    - Sliding window and no need for a queue here, because sum statistics are easy
    to update.

    Examples
    --------
    >>> p1456("abciiidef", 3)
    3
    >>> p1456("aeiou", 2)
    2
    >>> p1456("leetcode", 3)
    2
    >>> p1456("rhythms", 4)
    0
    >>> p1456("tryhard", 4)
    1

    """
    vowels = set("aeiou")
    num_vowels = sum(c in vowels for c in s[:k])
    max_vowels = num_vowels
    for i in range(k, len(s)):
        if s[i - k] in vowels:
            num_vowels -= 1
        if s[i] in vowels:
            num_vowels += 1
        max_vowels = max(max_vowels, num_vowels)
    return max_vowels

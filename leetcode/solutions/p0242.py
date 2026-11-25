from collections import Counter


def p242(s: str, t: str) -> bool:
    """242. Valid Anagram https://leetcode.com/problems/valid-anagram/"""
    return Counter(s) == Counter(t)

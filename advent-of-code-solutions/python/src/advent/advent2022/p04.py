"""Camp Cleanup
https://adventofcode.com/2022/day/4
"""

import re


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    4
    """
    s = s.strip("\n")
    total = 0
    for line in s.splitlines():
        a, b, c, d = [int(x) for x in re.findall(r"\d+", line)]
        if (a <= c <= d <= b) or (c <= a <= b <= d):
            total += 1
    return total


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    6
    """
    s = s.strip("\n")
    total = 0
    for line in s.splitlines():
        a, b, c, d = [int(x) for x in re.findall(r"\d+", line)]
        if (a <= c <= b) or (c <= a <= d) or (a <= d <= b) or (c <= b <= d):
            total += 1
    return total


test_string = """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
21-21,21-21
24-36,25-27
"""

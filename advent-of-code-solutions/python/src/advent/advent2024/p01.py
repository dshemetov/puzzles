"""1. https://adventofcode.com/2024/day/1"""

from collections import Counter


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    11
    """
    s = s.strip("\n")
    nums1 = [int(x.split()[0]) for x in s.splitlines()]
    nums1.sort()
    nums2 = [int(x.split()[1]) for x in s.splitlines()]
    nums2.sort()
    return sum(abs(x - y) for x, y in zip(nums1, nums2))


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    31
    """
    s = s.strip("\n")
    nums1 = [int(x.split()[0]) for x in s.splitlines()]
    counts = Counter(int(x.split()[1]) for x in s.splitlines())
    return sum(x * counts[x] for x in nums1)


test_string = """
3   4
4   3
2   5
1   3
3   9
3   3
"""

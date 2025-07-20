"""1. https://adventofcode.com/2024/day/1"""

import numpy as np


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    11
    """
    s = s.strip("\n")
    lines = [line.split() for line in s.splitlines()]
    data = np.array([[int(x) for x in line] for line in lines])

    data[:, 0].sort()
    data[:, 1].sort()

    return int(np.sum(np.abs(data[:, 0] - data[:, 1])))


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    31
    """
    s = s.strip("\n")
    lines = [line.split() for line in s.splitlines()]
    data = np.array([[int(x) for x in line] for line in lines])

    max_val = np.max(data)
    counts = np.bincount(data[:, 1], minlength=max_val + 1)

    return int(np.sum(data[:, 0] * counts[data[:, 0]]))


test_string = """
3   4
4   3
2   5
1   3
3   9
3   3
"""

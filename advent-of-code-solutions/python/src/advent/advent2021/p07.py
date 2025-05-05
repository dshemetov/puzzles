"""The Treachery of Whales
https://adventofcode.com/2021/day/7
"""

import numpy as np


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    37
    """
    nums = np.array(s.split(","), dtype=int)
    point = int(np.median(nums))
    return int(np.abs(point - nums).sum())


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    168
    """
    nums = np.array(s.split(","), dtype=int)
    positions = round(np.mean(nums)) + np.array([-1, 0, 1])
    return min(position_cost(n, nums) for n in positions)


def position_cost(n: int, nums: np.ndarray) -> int:
    return int(sum(m * (m + 1) // 2 for m in np.abs(n - nums)))


test_string = """16,1,2,0,4,2,7,1,2,14
"""

"""Lanternfish
https://adventofcode.com/2021/day/6
"""

from collections import Counter

import numpy as np


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    5934
    """
    fish_ages = parse_input(s)
    return get_number_fish_after_days(fish_ages, 80)


def parse_input(s: str) -> Counter:
    return Counter(int(x) for x in s.split(","))


def get_number_fish_after_days(fish_ages: Counter, n: int) -> int:
    """
    Examples:
    >>> get_number_fish_after_days(parse_input(test_string), 18)
    26
    """
    return int(pass_days(fish_ages, n).sum())


def pass_days(fish_ages: Counter, n: int = 1) -> np.ndarray:
    A = np.diag([1] * 8, k=1)
    A[8, 0] = A[6, 0] = 1
    v = np.array([fish_ages[i] for i in range(9)], dtype=int)
    for _ in range(n):
        v = A @ v
    return v


def solve_b(s: str) -> int:
    fish_ages = parse_input(s)
    return get_number_fish_after_days(fish_ages, 256)


test_string = """3,4,3,1,2
"""

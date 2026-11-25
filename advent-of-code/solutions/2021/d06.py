# /// script
# requires-python = ">=3.14"
# dependencies = ["numpy"]
# ///
"""Lanternfish
https://adventofcode.com/2021/day/6
"""

import sys
import time
from collections import Counter

import numpy as np


def part_a(s: str) -> int:
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


def part_b(s: str) -> int:
    fish_ages = parse_input(s)
    return get_number_fish_after_days(fish_ages, 256)


test_string = """3,4,3,1,2
"""


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

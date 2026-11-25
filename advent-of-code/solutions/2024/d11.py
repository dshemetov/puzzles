# /// script
# requires-python = ">=3.14"
# dependencies = ["numpy", "numba"]
# ///
"""11. https://adventofcode.com/2024/day/11"""

import sys
import time

import numpy as np
from numba import int64, njit
from numba.typed import Dict


@njit(cache=True)
def transform_int(n: int64):
    """Transform an integer based on its digit count."""
    if n == 0:
        return np.array([1], dtype=np.int64)

    # Count digits efficiently
    digits = 0
    temp = n
    while temp > 0:
        digits += 1
        temp //= 10

    if digits % 2 == 0:
        divisor = 10 ** (digits // 2)
        left = n // divisor
        right = n % divisor
        return np.array([left, right], dtype=np.int64)
    return np.array([n * 2024], dtype=np.int64)


@njit(int64(int64[:], int64), cache=True)
def main_loop(numbers: np.ndarray, iterations: int) -> int64:
    counts = Dict.empty(
        key_type=int64,
        value_type=int64,
    )
    for x in numbers:
        counts[x] = counts.get(x, 0) + 1
    for _ in range(iterations):
        new_counts = Dict.empty(
            key_type=int64,
            value_type=int64,
        )
        for num, count in counts.items():
            for new_num in transform_int(num):
                new_counts[new_num] = new_counts.get(new_num, 0) + count
        counts = new_counts
    total = 0
    for x in counts.values():
        total += x
    return total


def part_a(s: str) -> int:
    """
    Examples:
    >>> part_a(test_string)
    55312
    """
    numbers = np.array(s.strip("\n").split(), dtype=np.int64)
    return main_loop(numbers, 25)


def part_b(s: str) -> int:
    """
    Examples:
    >>> part_b(test_string)
    65601038650482
    """
    numbers = np.array(s.strip("\n").split(), dtype=np.int64)
    return main_loop(numbers, 75)


test_string = """
125 17
"""


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

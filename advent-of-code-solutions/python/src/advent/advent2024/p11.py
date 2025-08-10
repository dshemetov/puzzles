"""11. https://adventofcode.com/2024/day/11"""

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


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    55312
    """
    numbers = np.array(s.strip("\n").split(), dtype=np.int64)
    return main_loop(numbers, 25)


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    65601038650482
    """
    numbers = np.array(s.strip("\n").split(), dtype=np.int64)
    return main_loop(numbers, 75)


test_string = """
125 17
"""

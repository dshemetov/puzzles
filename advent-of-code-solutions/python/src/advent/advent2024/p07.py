"""7. https://adventofcode.com/2024/day/7"""

import re

import numba as nb
import numpy as np
from numba import boolean, int64


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    3749
    """
    s = s.strip("\n")
    lines = [[int(x) for x in re.findall(r"\d+", x)] for x in s.splitlines()]

    total = 0
    for line in lines:
        if backtrack(line[0], len(line[1:]) - 1, line[1:], False):
            total += line[0]

    return total


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    11387
    """
    s = s.strip("\n")
    lines = [[int(x) for x in re.findall(r"\d+", x)] for x in s.splitlines()]

    total = 0
    for line in lines:
        if backtrack(line[0], len(line[1:]) - 1, line[1:], True):
            total += line[0]

    return total


def backtrack(target: int, idx: int, numbers: list[int], with_combination: bool) -> bool:
    if idx == 0:
        return target == numbers[0]

    current_num = numbers[idx]

    # Try subtraction (reverse of addition)
    if target > current_num and backtrack(target - current_num, idx - 1, numbers, with_combination):
        return True

    # Try division (reverse of multiplication)
    if target % current_num == 0 and backtrack(target // current_num, idx - 1, numbers, with_combination):
        return True

    # Try de-concatenation (reverse of concatenation)
    if with_combination:
        num_str = str(current_num)
        target_str = str(target)
        if len(target_str) > len(num_str) and target_str.endswith(num_str):
            new_target_str = target_str[: -len(num_str)]
            if new_target_str:
                new_target = int(new_target_str)
                if backtrack(new_target, idx - 1, numbers, with_combination):
                    return True

    return False


# The numba version does not improve performance. The algorithm is fast enough.
@nb.njit(boolean(int64, int64, int64[:], boolean), cache=True)
def backtrack_numba(target, idx, numbers, with_combination):
    if idx == 0:
        return target == numbers[0]

    current_num = numbers[idx]

    # Try subtraction (reverse of addition)
    if target > current_num and backtrack_numba(target - current_num, idx - 1, numbers, with_combination):
        return True

    # Try division (reverse of multiplication)
    if target % current_num == 0 and backtrack_numba(target // current_num, idx - 1, numbers, with_combination):
        return True

    # Try de-concatenation (reverse of concatenation)
    # Purely numeric approach because, while Numba supports string operations,
    # it doesn't support casting to int from string.
    if with_combination:
        # Pure numeric approach: check if target ends with current_num
        # We need to find the number of digits in current_num
        temp = current_num
        num_digits = 0
        while temp > 0:
            temp //= 10
            num_digits += 1

        if num_digits > 0:
            # Calculate the divisor to get the prefix
            divisor = 10**num_digits
            # Check if target ends with current_num
            if target % divisor == current_num:
                # Get the prefix by integer division
                prefix = target // divisor
                if prefix > 0 and backtrack_numba(prefix, idx - 1, numbers, with_combination):
                    return True

    return False


def solve_a_numba(s: str) -> int:
    s = s.strip("\n")
    lines = [[int(x) for x in re.findall(r"\d+", x)] for x in s.splitlines()]

    total = 0
    for line in lines:
        # Convert to numpy array for Numba
        numbers = np.array(line[1:], dtype=np.int64)
        if backtrack_numba(line[0], len(numbers) - 1, numbers, False):
            total += line[0]

    return total


def solve_b_numba(s: str) -> int:
    s = s.strip("\n")
    lines = [[int(x) for x in re.findall(r"\d+", x)] for x in s.splitlines()]

    total = 0
    for line in lines:
        numbers = np.array(line[1:], dtype=np.int64)
        if backtrack_numba(line[0], len(numbers) - 1, numbers, True):
            total += line[0]

    return total


test_string = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

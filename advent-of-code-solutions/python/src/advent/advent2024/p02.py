"""2. https://adventofcode.com/2024/day/2"""

import numpy as np


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    2
    """
    s = s.strip("\n")
    total = 0

    for line in s.splitlines():
        nums = np.array([int(x) for x in line.split()])
        diffs = np.diff(nums)
        all_increasing = np.all(diffs >= 0)
        all_decreasing = np.all(diffs <= 0)
        changes_bounded = np.all((diffs >= -3) & (diffs <= 3) & (diffs != 0))

        if (all_increasing or all_decreasing) and changes_bounded:
            total += 1

    return total


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    4
    """
    s = s.strip("\n")
    total = 0

    for line in s.splitlines():
        nums = np.array([int(x) for x in line.split()])
        diffs = np.diff(nums)
        all_increasing = np.all(diffs >= 0)
        all_decreasing = np.all(diffs <= 0)
        changes_bounded = np.all((diffs >= -3) & (diffs <= 3) & (diffs != 0))

        if (all_increasing or all_decreasing) and changes_bounded:
            total += 1
            continue

        # Try removing one element at a time
        for j in range(len(nums)):
            new_nums = np.concatenate([nums[:j], nums[j+1:]])

            if len(new_nums) < 2:
                continue

            new_diffs = np.diff(new_nums)
            new_all_increasing = np.all(new_diffs >= 0)
            new_all_decreasing = np.all(new_diffs <= 0)
            new_changes_bounded = np.all((new_diffs >= -3) & (new_diffs <= 3) & (new_diffs != 0))

            if (new_all_increasing or new_all_decreasing) and new_changes_bounded:
                total += 1
                break

    return total


test_string = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

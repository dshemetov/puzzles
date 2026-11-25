# /// script
# requires-python = ">=3.14"
# dependencies = ["numpy"]
# ///
"""2. https://adventofcode.com/2024/day/2"""

import sys
import time

import numpy as np


def part_a(s: str) -> int:
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


def part_b(s: str) -> int:
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
            new_nums = np.concatenate([nums[:j], nums[j + 1 :]])

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


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

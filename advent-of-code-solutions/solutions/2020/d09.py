# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""https://adventofcode.com/2020/day/9"""

import sys
import time


def part_a(s: str) -> int:
    nums = [int(line) for line in s.split("\n")]
    for i, x in enumerate(nums):
        if i < 25:
            continue
        valid_nums = make_pairs(nums[i - 25 : i])
        if x not in valid_nums:
            break
    return x


def make_pairs(nums):
    from itertools import product

    return set([x + y for x, y in product(nums, repeat=2) if x != y])


def part_b(s: str) -> int:
    nums = [int(line) for line in s.split("\n")]
    for i in range(len(nums)):
        for j in range(i, len(nums)):
            if sum(nums[i:j]) == 138879426:
                return max(nums[i:j]) + min(nums[i:j])


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

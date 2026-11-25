# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""https://adventofcode.com/2020/day/1"""

import sys
import time
from itertools import combinations


def part_a(s: str) -> int:
    nums = [int(n) for n in s.split("\n")]
    return next(x * y for x, y in combinations(nums, 2) if x + y == 2020)


def part_b(s: str) -> int:
    nums = [int(n) for n in s.split("\n")]
    return next(x * y * z for x, y, z in combinations(nums, 3) if x + y + z == 2020)


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

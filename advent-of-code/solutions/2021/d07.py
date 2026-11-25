# /// script
# requires-python = ">=3.14"
# dependencies = ["numpy"]
# ///
"""The Treachery of Whales
https://adventofcode.com/2021/day/7
"""

import sys
import time

import numpy as np


def part_a(s: str) -> int:
    nums = np.array(s.split(","), dtype=int)
    point = int(np.median(nums))
    return int(np.abs(point - nums).sum())


def part_b(s: str) -> int:
    nums = np.array(s.split(","), dtype=int)
    positions = round(np.mean(nums)) + np.array([-1, 0, 1])
    return min(position_cost(n, nums) for n in positions)


def position_cost(n: int, nums: np.ndarray) -> int:
    return int(sum(m * (m + 1) // 2 for m in np.abs(n - nums)))


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

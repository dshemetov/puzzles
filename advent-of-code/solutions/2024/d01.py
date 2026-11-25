# /// script
# requires-python = ">=3.14"
# dependencies = ["numpy"]
# ///
"""1. https://adventofcode.com/2024/day/1"""

import sys
import time

import numpy as np


def part_a(s: str) -> int:
    s = s.strip("\n")
    lines = [line.split() for line in s.splitlines()]
    data = np.array([[int(x) for x in line] for line in lines])

    data[:, 0].sort()
    data[:, 1].sort()

    return int(np.sum(np.abs(data[:, 0] - data[:, 1])))


def part_b(s: str) -> int:
    s = s.strip("\n")
    lines = [line.split() for line in s.splitlines()]
    data = np.array([[int(x) for x in line] for line in lines])

    max_val = np.max(data)
    counts = np.bincount(data[:, 1], minlength=max_val + 1)

    return int(np.sum(data[:, 0] * counts[data[:, 0]]))


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

# /// script
# requires-python = ">=3.14"
# dependencies = ["numpy"]
# ///
"""https://adventofcode.com/2020/day/3"""

import sys
import time
import numpy as np


def part_a(s: str) -> int:
    mat = np.array([list(line) for line in s.split("\n")])
    n, m = mat.shape
    mat = np.pad(mat, pad_width=[(0, 0), (0, 3 * n)], mode="wrap")
    return sum(1 if mat[i, 3 * i] == "#" else 0 for i in range(n))


def part_b(s: str) -> int:
    mat = np.array([list(line) for line in s.split("\n")])
    n, m = mat.shape
    mat = np.pad(mat, pad_width=[(0, 0), (0, 7 * n)], mode="wrap")
    trees_slope_11 = sum(1 if mat[i, i] == "#" else 0 for i in range(n))
    trees_slope_31 = sum(1 if mat[i, 3 * i] == "#" else 0 for i in range(n))
    trees_slope_51 = sum(1 if mat[i, 5 * i] == "#" else 0 for i in range(n))
    trees_slope_71 = sum(1 if mat[i, 7 * i] == "#" else 0 for i in range(n))
    trees_slope_12 = sum(1 if mat[2 * i, i] == "#" else 0 for i in range(n // 2))
    return trees_slope_11 * trees_slope_31 * trees_slope_51 * trees_slope_71 * trees_slope_12


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

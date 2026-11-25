# /// script
# requires-python = ">=3.14"
# dependencies = ["numpy"]
# ///
"""Binary Diagnostics
https://adventofcode.com/2021/day/3
"""

import sys
import time
from copy import copy

import numpy as np


def binary_to_int(ls: list[int]) -> int:
    """Convert a list of 0's and 1's to an integer.

    Examples:
    >>> binary_to_int([1, 0, 1])
    5
    """
    return int("".join(str(i) for i in ls), 2)


def part_a(s: str) -> int:
    mat = np.array([list(line) for line in s.strip("\n").split("\n")], dtype=int)
    n, _ = mat.shape
    max_rows = mat.sum(axis=0) >= n / 2
    min_rows = ~max_rows
    max_rows = max_rows.astype(int)
    min_rows = min_rows.astype(int)
    gamma_rate, epsilon_rate = binary_to_int(max_rows), binary_to_int(min_rows)
    return gamma_rate * epsilon_rate


def part_b(s: str) -> int:
    mat = np.array([list(line) for line in s.strip("\n").split("\n")], dtype=int)
    _, m = mat.shape

    mat_ = copy(mat)
    for ix in range(m):
        if len(mat_) == 1:
            break
        n, _ = mat_.shape
        mat_ = mat_[mat_[:, ix] == int(mat_[:, ix].sum() >= n / 2)]
    oxygen_rating = binary_to_int(mat_[0])

    mat_ = copy(mat)
    for ix in range(m):
        if len(mat_) == 1:
            break
        n, _ = mat_.shape
        mat_ = mat_[mat_[:, ix] == int(mat_[:, ix].sum() < n / 2)]
    co2_rating = binary_to_int(mat_[0])

    return oxygen_rating * co2_rating


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

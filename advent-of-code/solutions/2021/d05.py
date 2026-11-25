# /// script
# requires-python = ">=3.14"
# dependencies = ["numpy"]
# ///
"""Hydrothermal Venture Giant Squid
https://adventofcode.com/2021/day/5
"""

import sys
import time
import re

import numpy as np


def part_a(s: str) -> int:
    """
    Examples:
    >>> part_a(test_string)
    5
    """
    matches = (m.groups() for m in re.finditer(r"(\d+),(\d+) -> (\d+),(\d+)", s))
    lines = np.array([[(x1, y1), (x2, y2)] for x1, y1, x2, y2 in matches], dtype=int)
    n, m = lines.max(axis=(0, 1)) + 1
    grid = np.zeros((n, m))

    for pt1, pt2 in lines:
        if (pt1 == pt2).any():
            xs, ys = make_line(pt1, pt2).T
            grid[xs, ys] += 1

    return int((grid > 1).sum())


def make_line(pt1: np.ndarray, pt2: np.ndarray) -> np.ndarray:
    n = np.abs(pt1 - pt2).max()
    d = (pt1 - pt2) // n
    return np.vstack([pt2 + d * i for i in range(n + 1)])


def get_intersection(line1: np.ndarray, line2: np.ndarray) -> np.ndarray:
    (x1, y1), (x2, y2) = line1
    (v1, w1), (v2, w2) = line2
    t, s = np.linalg.inv(np.array([[x2 - x1, v1 - v2], [y2 - y1, w1 - w2]])) @ np.array([v1 - x1, w1 - y1])
    return (1 - t) * line1[0] + t * line1[1]


def part_b(s: str) -> int:
    """
    Examples:
    >>> part_b(test_string)
    12
    """
    matches = (m.groups() for m in re.finditer(r"(\d+),(\d+) -> (\d+),(\d+)", s))
    mat = np.array([[(x1, y1), (x2, y2)] for x1, y1, x2, y2 in matches], dtype=int)
    n, m = mat.max(axis=(0, 1)) + 1
    grid = np.zeros((n, m))

    for pt1, pt2 in mat:
        xs, ys = make_line(pt1, pt2).T
        grid[xs, ys] += 1

    return int((grid > 1).sum())


test_string = """0,9 -> 5,9
8,0 -> 0,8
9,4 -> 3,4
2,2 -> 2,1
7,0 -> 7,4
6,4 -> 2,0
0,9 -> 2,9
3,4 -> 1,4
0,0 -> 8,8
5,5 -> 8,2"""


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

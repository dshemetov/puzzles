# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Smoke Basin
https://adventofcode.com/2021/day/9
"""

import sys
import time
from bisect import insort
from collections.abc import Iterable


def nlargest(n: int, it: Iterable) -> list:
    """
    Examples:
    >>> nlargest(5, [5, 4, 3, 10, 2, 5])
    [3, 4, 5, 5, 10]
    """
    top_n = []
    for e in it:
        insort(top_n, e)
        if len(top_n) > n:
            top_n.pop(0)
    return top_n


def part_a(s: str) -> int:
    mat = [list(x) for x in s.strip("\n").split("\n")]
    n, m = len(mat), len(mat[0])
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    total = 0
    for i in range(n):
        for j in range(m):
            for i_, j_ in [(i + i__, j + j__) for i__, j__ in directions]:
                if 0 <= i_ < len(mat) and 0 <= j_ < len(mat[0]):
                    if mat[i_][j_] <= mat[i][j]:
                        break
            else:
                total += int(mat[i][j]) + 1
    return total


def part_b(s: str) -> int:
    mat = [list(x) for x in s.strip("\n").split("\n")]
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]

    visited = set()
    basin_sizes = []
    for i in range(len(mat)):
        for j in range(len(mat[0])):
            if mat[i][j] == "9":
                continue
            if (i, j) in visited:
                continue

            basin_size = 0
            stack = [(i, j)]
            while stack:
                i_, j_ = stack.pop()
                if mat[i_][j_] == "9":
                    continue
                if (i_, j_) in visited:
                    continue
                visited.add((i_, j_))
                basin_size += 1
                for i__, j__ in [(i_ + i___, j_ + j___) for i___, j___ in directions]:
                    if 0 <= i__ < len(mat) and 0 <= j__ < len(mat[0]):
                        stack.append((i__, j__))

            basin_sizes.append(basin_size)

    a, b, c = nlargest(3, basin_sizes)
    return a * b * c


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

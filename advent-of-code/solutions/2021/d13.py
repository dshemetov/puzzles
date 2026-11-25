# /// script
# requires-python = ">=3.14"
# dependencies = ["numpy"]
# ///
"""Transparent Origami https://adventofcode.com/2021/day/13"""

import sys
import time
import re

import numpy as np


def part_a(s: str) -> int:
    ixs, folds = s.split("\n\n")
    ixs = np.array([line.split(",") for line in ixs.strip("\n").split("\n")], dtype=int)[:, ::-1].T
    n, m = ixs.max(axis=1) + 1
    mat = np.zeros((n, m), dtype=bool)
    mat[ixs[0], ixs[1]] = True

    folds = [re.match(r"fold along (\w)=(\d+)", line).groups() for line in folds.split("\n")][0:1]
    for along, _ in folds:
        mat = fold_mat(along, mat)

    return int(mat.sum())


def fold_mat(along: str, mat: list[list[str]]) -> list[list[str]]:
    n, m = mat.shape
    if along == "y":
        new_mat = mat[0 : n // 2, :] | mat[: n // 2 : -1, :]
    if along == "x":
        new_mat = mat[:, 0 : m // 2] | mat[:, : m // 2 : -1]
    return new_mat


def part_b(s: str) -> int:
    ixs, folds = s.split("\n\n")
    ixs = [line.split(",") for line in ixs.strip("\n").split("\n")]
    ixs = [(int(x), int(y)) for y, x in ixs]

    n, m = max(x for x, _ in ixs) + 1, max(y for _, y in ixs) + 1
    mat = np.zeros((n, m), dtype=bool)
    for i, j in ixs:
        mat[i][j] = True

    folds = [re.match(r"fold along (\w)=(\d+)", line).groups() for line in folds.split("\n")]
    for along, _ in folds:
        mat = fold_mat(along, mat)
    print("\n".join(["".join(["1" if x else " " for x in row]) for row in mat]))
    return 0


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

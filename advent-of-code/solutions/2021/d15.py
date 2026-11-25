# /// script
# requires-python = ">=3.14"
# dependencies = ["numpy"]
# ///
"""Chiton https://adventofcode.com/2021/day/15"""

import sys
import time
from heapq import heappop, heappush

import numpy as np


def part_a(s: str) -> int:
    mat = np.array([list(line) for line in s.split("\n")], dtype=int)
    n, m = mat.shape
    actual_cost, _ = get_minimum_path(mat, (0, 0), (n - 1, m - 1))
    return int(actual_cost)


def get_minimum_path(mat: np.ndarray, start_ix: tuple[int, int], end_ix: tuple[int, int]) -> np.ndarray:
    ix = start_ix
    cost = 0
    priority_queue = []
    best_cost = {}
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    while end_ix != ix:
        for ix_ in [(ix[0] + directions[0], ix[1] + directions[1]) for directions in directions]:
            if not (0 <= ix_[0] < mat.shape[0] and 0 <= ix_[1] < mat.shape[1]):
                continue
            cost_ = cost + mat[ix_]
            if ix_ in best_cost and best_cost[ix_] <= cost_:
                continue
            best_cost[ix_] = min(best_cost.get(ix_, cost_), cost_)
            heappush(priority_queue, (cost_, ix_))
        cost, ix = heappop(priority_queue)

    return cost, ix


def part_b(s: str) -> int:
    mat = np.array([list(line) for line in s.split("\n")], dtype=int)
    big_mat = expand_mat(mat)
    n, m = big_mat.shape
    actual_cost, _ = get_minimum_path(big_mat, (0, 0), (n - 1, m - 1))
    return int(actual_cost)


def expand_mat(mat):
    n, _ = mat.shape
    ntile = 5
    nxp = ntile * n
    graph_tiled = np.zeros((nxp, nxp), dtype=int)
    for xtile in range(ntile):
        for ytile in range(ntile):
            xs, ys = xtile * n, ytile * n
            xe, ye = (xtile + 1) * n, (ytile + 1) * n
            graph_tiled[xs:xe, ys:ye] = (mat + xtile + ytile - 1) % 9 + 1

    return graph_tiled


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

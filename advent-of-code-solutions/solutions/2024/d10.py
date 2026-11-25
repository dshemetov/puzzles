# /// script
# requires-python = ">=3.14"
# dependencies = ["numpy", "numba"]
# ///
"""10. https://adventofcode.com/2024/day/10"""

import sys
import time

import numpy as np
from numba import int32, int64, njit


@njit(int64(int32[:, :], int32, int32, int32[:, :], int32, int32))
def count_paths_to_nines(grid: np.ndarray, curr_i: int, curr_j: int, visited: np.ndarray, m: int, n: int) -> int:
    # If we've reached a 9, count this path
    if grid[curr_i, curr_j] == 9:
        return 1

    # Mark current position as visited
    visited[curr_i, curr_j] = 1
    total_paths = 0

    # Try all 4 directions
    for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        next_i, next_j = curr_i + di, curr_j + dj

        # Check bounds
        if not (0 <= next_i < m and 0 <= next_j < n):
            continue

        # Check if value increases by 1
        if grid[next_i, next_j] - grid[curr_i, curr_j] != 1:
            continue

        # Check if not already visited
        if visited[next_i, next_j] == 0:
            total_paths += count_paths_to_nines(grid, next_i, next_j, visited, m, n)

    # Backtrack: remove current position from visited
    visited[curr_i, curr_j] = 0

    return total_paths


def find_reachable_nines(
    grid: np.ndarray,
    start_i: int,
    start_j: int,
    curr_i: int,
    curr_j: int,
    reachable_pairs: set,
    visited: np.ndarray,
    m: int,
    n: int,
):
    # If we've reached a 9, add the start-end pair
    if grid[curr_i, curr_j] == 9:
        reachable_pairs.add((start_i, start_j, curr_i, curr_j))
        return

    # Mark current position as visited
    visited[curr_i, curr_j] = 1

    # Try all 4 directions
    for di, dj in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        next_i, next_j = curr_i + di, curr_j + dj

        # Check bounds
        if not (0 <= next_i < m and 0 <= next_j < n):
            continue

        # Check if value increases by 1
        if grid[next_i, next_j] - grid[curr_i, curr_j] != 1:
            continue

        # Check if not already visited
        if visited[next_i, next_j] == 0:
            find_reachable_nines(grid, start_i, start_j, next_i, next_j, reachable_pairs, visited, m, n)

    # Backtrack: remove current position from visited
    visited[curr_i, curr_j] = 0


def part_a(s: str) -> int:
    """
    Examples:
    >>> part_a(test_string)
    36
    """
    s = s.strip("\n")
    lines = s.splitlines()
    grid = np.array([[int(c) for c in line] for line in lines], dtype=np.int8)
    m, n = grid.shape
    reachable_pairs = set()
    starts = [(i, j) for j in range(n) for i in range(m) if grid[i, j] == 0]

    for start_i, start_j in starts:
        visited = np.zeros((m, n), dtype=np.int32)
        find_reachable_nines(grid, start_i, start_j, start_i, start_j, reachable_pairs, visited, m, n)

    return len(reachable_pairs)


def part_b(s: str) -> int:
    """
    Examples:
    >>> part_b(test_string)
    81
    """
    s = s.strip("\n")
    lines = s.splitlines()
    grid = np.array([[int(c) for c in line] for line in lines], dtype=np.int32)

    return solve_b_numba(grid)


@njit(int64(int32[:, :]))
def solve_b_numba(grid: np.ndarray) -> int:
    m, n = grid.shape
    starts = [(i, j) for j in range(n) for i in range(m) if grid[i, j] == 0]

    total = 0
    for start_i, start_j in starts:
        visited = np.zeros((m, n), dtype=np.int32)
        total += count_paths_to_nines(grid, start_i, start_j, visited, m, n)

    return total


test_string = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

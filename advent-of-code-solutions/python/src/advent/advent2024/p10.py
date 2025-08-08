"""10. https://adventofcode.com/2024/day/10"""

import numba as nb
import numpy as np
from numba import int8, int32, int64


@nb.njit(int64(int8[:, :], int32, int32, int8[:, :], int32, int32), cache=True)
def count_paths_to_nines_recursive(
    grid: np.ndarray, curr_i: int, curr_j: int, visited: np.ndarray, m: int, n: int
) -> int:
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
            total_paths += count_paths_to_nines_recursive(grid, next_i, next_j, visited, m, n)

    # Backtrack: remove current position from visited
    visited[curr_i, curr_j] = 0

    return total_paths


def find_reachable_nines_recursive(
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
            find_reachable_nines_recursive(grid, start_i, start_j, next_i, next_j, reachable_pairs, visited, m, n)

    # Backtrack: remove current position from visited
    visited[curr_i, curr_j] = 0


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    36
    """
    s = s.strip("\n")
    lines = s.splitlines()
    grid = np.array([[int(c) for c in line] for line in lines], dtype=np.int8)

    m, n = grid.shape
    reachable_pairs = set()

    # Find all starting positions (value 0)
    starts = [(i, j) for j in range(n) for i in range(m) if grid[i, j] == 0]

    # For each starting position, find all reachable 9's
    for start_i, start_j in starts:
        visited = np.zeros((m, n), dtype=np.bool)
        find_reachable_nines_recursive(grid, start_i, start_j, start_i, start_j, reachable_pairs, visited, m, n)

    return len(reachable_pairs)


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    81
    """
    s = s.strip("\n")
    lines = s.splitlines()
    grid = np.array([[int(c) for c in line] for line in lines], dtype=np.int8)

    return solve_b_numba(grid)


@nb.njit(int64(int8[:, :]), cache=True)
def solve_b_numba(grid: np.ndarray) -> int:
    m, n = grid.shape
    total = 0

    # Find all starting positions (value 0)
    starts = [(i, j) for j in range(n) for i in range(m) if grid[i, j] == 0]

    # For each starting position, count all paths to 9's
    for start_i, start_j in starts:
        visited = np.zeros((m, n), dtype=np.int8)
        total += count_paths_to_nines_recursive(grid, start_i, start_j, visited, m, n)

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

"""20. https://adventofcode.com/2024/day/20"""

from collections import deque

import numpy as np
from numba import int64, njit


def maze_solver(
    grid: np.ndarray, s: tuple[int, int], t: tuple[int, int]
) -> tuple[int, dict[tuple[int, int], tuple[int, int]]]:
    """BFS to find shortest path from s to t in grid."""
    m, n = grid.shape
    queue = deque([(0, s[0], s[1])])
    visited = set()
    prev_map = {}

    while queue:
        dist, x, y = queue.popleft()
        if x == t[0] and y == t[1]:
            return dist, prev_map

        for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            nx, ny = x + dx, y + dy
            if 1 <= nx <= m and 1 <= ny <= n and grid[nx - 1, ny - 1] != "#" and (nx, ny) not in visited:
                queue.append((dist + 1, nx, ny))
                prev_map[(nx, ny)] = (x, y)
                visited.add((nx, ny))

    return 0, prev_map


@njit(int64(int64[:, :], int64, int64), cache=True)
def pairwise_cheat_solver(path: np.ndarray, radius: int, time_diff_thresh: int) -> int:
    """Count cheats by checking pairs of points along the path."""
    n = len(path)
    cheats = 0
    for j in range(time_diff_thresh, n):
        for i in range(j - time_diff_thresh):
            x1, y1 = path[i, 0], path[i, 1]
            x2, y2 = path[j, 0], path[j, 1]
            distance = abs(x1 - x2) + abs(y1 - y2)
            if distance <= radius and j - i - distance >= time_diff_thresh:
                cheats += 1

    return cheats


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    1
    """
    s = s.strip("\n")
    if s == test_string.strip("\n"):
        time_diff_thresh = 50
    else:
        time_diff_thresh = 100
    radius = 2

    # Parse grid
    grid_lines = s.strip().split("\n")
    grid = np.array([list(line) for line in grid_lines])

    # Find start and end positions
    st = (int(np.where(grid == "S")[0][0] + 1), int(np.where(grid == "S")[1][0] + 1))
    ta = (int(np.where(grid == "E")[0][0] + 1), int(np.where(grid == "E")[1][0] + 1))

    # Get maze path (there's only one)
    dist, prev_map = maze_solver(grid, st, ta)
    path = []
    current = ta
    while current != st:
        path.append(current)
        current = prev_map[current]
    path.append(st)
    path.reverse()
    path = np.array(path, dtype=np.int64)

    return pairwise_cheat_solver(path, radius, time_diff_thresh)


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    285
    """
    s = s.strip("\n")
    if s == test_string.strip("\n"):
        time_diff_thresh = 50
    else:
        time_diff_thresh = 100
    radius = 20

    grid_lines = s.strip().split("\n")
    grid = np.array([list(line) for line in grid_lines])

    # Find start and end positions
    st = (int(np.where(grid == "S")[0][0] + 1), int(np.where(grid == "S")[1][0] + 1))
    ta = (int(np.where(grid == "E")[0][0] + 1), int(np.where(grid == "E")[1][0] + 1))

    # Get maze path (there's only one)
    dist, prev_map = maze_solver(grid, st, ta)
    path = []
    current = ta
    while current != st:
        path.append(current)
        current = prev_map[current]
    path.append(st)
    path.reverse()
    path = np.array(path, dtype=np.int64)

    return pairwise_cheat_solver(path, radius, time_diff_thresh)


test_string = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""

"""14. https://adventofcode.com/2023/day/14"""

import numpy as np


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    136
    """
    s = s.strip("\n")
    grid = np.array([list(line) for line in s.split("\n")], dtype=str)
    # Tilt rocks north.
    grid = tilt_rocks(grid, (-1, 0))
    return get_score(grid)


def tilt_rocks(grid: np.ndarray, dv: tuple[int, int]) -> np.ndarray:
    m, n = grid.shape
    di, dj = dv
    # If we move rocks up, we should start from the top.
    h_iter = range(m) if di == -1 else range(m - 1, -1, -1)
    v_iter = range(n) if dj == -1 else range(n - 1, -1, -1)
    for i in h_iter:
        for j in v_iter:
            # Find rocks.
            if grid[i, j] != "O":
                continue
            # Try to move the rock.
            temp_i, temp_j = i, j
            while 0 <= temp_i + di < m and 0 <= temp_j + dj < n and grid[temp_i + di, temp_j + dj] == ".":
                temp_i += di
                temp_j += dj
            # If it can't move, it's in a stable position.
            if temp_i == i and temp_j == j:
                continue
            # Otherwise, move it.
            grid[temp_i, temp_j] = "O"
            grid[i, j] = "."
    return grid


def get_score(grid: np.ndarray) -> int:
    m, n = grid.shape
    score = 0
    for i in range(m):
        for j in range(n):
            if grid[i, j] != "O":
                continue
            score += m - i
    return score


def get_hash(grid: np.ndarray) -> str:
    return "\n".join(["".join(row) for row in grid])


def get_grid_from_hash(s: str) -> np.ndarray:
    return np.array([list(line) for line in s.split("\n")], dtype=str)


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    64
    """
    s = s.strip("\n")
    grid = np.array([list(line) for line in s.split("\n")], dtype=str)
    dirs = [(-1, 0), (0, -1), (1, 0), (0, 1)]
    # Store grid hashes to detect cycles.
    hs = []
    num_cycles = 1000000000
    for i in range(num_cycles):
        # Tilt rocks north, west, south, east.
        grid = grid.copy()
        grid = tilt_rocks(grid, dirs[0])
        grid = tilt_rocks(grid, dirs[1])
        grid = tilt_rocks(grid, dirs[2])
        grid = tilt_rocks(grid, dirs[3])
        h = get_hash(grid)
        if h in hs:
            # print(f"Cycle detected at {i}")
            # Now we can figure out the cycle length.
            start_idx = hs.index(h)
            num_cycles -= start_idx
            hs = hs[start_idx:]
            break
        hs.append(h)

    # So now we know the cycle length.
    final_grid = get_grid_from_hash(hs[(num_cycles - 1) % len(hs)])
    return get_score(final_grid)


test_string = """
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
"""

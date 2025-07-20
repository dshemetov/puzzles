"""8. https://adventofcode.com/2024/day/8"""

import numba as nb
import numpy as np
from numba import int32


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    14
    """
    s = s.strip("\n")
    lines = s.splitlines()

    # Find the maximum length of any row
    max_len = max(len(line) for line in lines)

    # Pad shorter rows with dots
    padded_lines = [line + "." * (max_len - len(line)) for line in lines]

    grid = np.array([[ord(c) for c in row] for row in padded_lines], dtype=np.int32)
    m, n = grid.shape
    return solve_a_numba(grid, m, n)


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    34
    """
    s = s.strip("\n")
    lines = s.splitlines()

    # Find the maximum length of any row
    max_len = max(len(line) for line in lines)

    # Pad shorter rows with dots
    padded_lines = [line + "." * (max_len - len(line)) for line in lines]

    grid = np.array([[ord(c) for c in row] for row in padded_lines], dtype=np.int32)
    m, n = grid.shape
    return solve_b_numba(grid, m, n)


@nb.njit(int32(int32[:, :], int32, int32), cache=True)
def solve_a_numba(grid: np.ndarray, m: int, n: int) -> int:
    antinodes = np.zeros((m, n), dtype=np.bool_)

    total = 0
    for char in range(ord("0"), ord("z") + 1):
        positions = [(i, j) for i in range(m) for j in range(n) if grid[i, j] == char]

        num_antennas = len(positions)
        for i in range(num_antennas):
            for j in range(i + 1, num_antennas):
                pos1_i, pos1_j = positions[i]
                pos2_i, pos2_j = positions[j]

                dx = pos2_i - pos1_i
                dy = pos2_j - pos1_j

                # Check one direction
                x, y = pos2_i + dx, pos2_j + dy
                if 0 <= x < m and 0 <= y < n and not antinodes[x, y]:
                    antinodes[x, y] = True
                    total += 1

                # Check opposite direction
                x, y = pos1_i - dx, pos1_j - dy
                if 0 <= x < m and 0 <= y < n and not antinodes[x, y]:
                    antinodes[x, y] = True
                    total += 1

    return total


@nb.njit(int32(int32[:, :], int32, int32), cache=True)
def solve_b_numba(grid: np.ndarray, m: int, n: int) -> int:
    # Use boolean array to track antinodes
    antinodes = np.zeros((m, n), dtype=np.bool_)

    for char in range(ord("0"), ord("z") + 1):
        positions = [(i, j) for i in range(m) for j in range(n) if grid[i, j] == char]

        num_antennas = len(positions)
        for i in range(num_antennas):
            for j in range(i + 1, num_antennas):
                pos1_i, pos1_j = positions[i]
                pos2_i, pos2_j = positions[j]

                dx = pos2_i - pos1_i
                dy = pos2_j - pos1_j

                # Add the antenna positions themselves
                antinodes[pos1_i, pos1_j] = True
                antinodes[pos2_i, pos2_j] = True

                # Check one direction (extending the line)
                x, y = pos2_i + dx, pos2_j + dy
                while 0 <= x < m and 0 <= y < n:
                    antinodes[x, y] = True
                    x, y = x + dx, y + dy

                # Check opposite direction (extending the line)
                x, y = pos1_i - dx, pos1_j - dy
                while 0 <= x < m and 0 <= y < n:
                    antinodes[x, y] = True
                    x, y = x - dx, y - dy

    return np.sum(antinodes)


test_string = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

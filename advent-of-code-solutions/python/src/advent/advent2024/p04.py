"""4. https://adventofcode.com/2024/day/4"""

import numpy as np


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    18
    """
    s = s.strip("\n")
    grid = np.array([list(row) for row in s.split("\n")])
    m, n = grid.shape
    total = 0

    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]

    for i in range(m):
        for j in range(n):
            for dx, dy in directions:
                for sgn in [1, -1]:
                    valid = True
                    for k in range(4):
                        x, y = i + sgn * k * dx, j + sgn * k * dy
                        if not (0 <= x < m and 0 <= y < n):
                            valid = False
                            break
                    if not valid:
                        continue

                    if (grid[i, j] == 'X' and
                        grid[i + sgn * dx, j + sgn * dy] == 'M' and
                        grid[i + sgn * 2 * dx, j + sgn * 2 * dy] == 'A' and
                        grid[i + sgn * 3 * dx, j + sgn * 3 * dy] == 'S'):
                        total += 1

    return total


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    9
    """
    s = s.strip("\n")
    grid = np.array([list(row) for row in s.split("\n")])
    m, n = grid.shape
    total = 0

    for i in range(1, m - 1):
        for j in range(1, n - 1):
            valid = True
            for k in [-1, 0, 1]:
                if not (0 <= i - k < m and 0 <= j + k < n and
                       0 <= i + k < m and 0 <= j + k < n):
                    valid = False
                    break
            if not valid:
                continue

            # Up-right diagonal: (i-k, j+k)
            upright_mas = (grid[i-1, j+1] == 'M' and grid[i, j] == 'A' and grid[i+1, j-1] == 'S')
            upright_sam = (grid[i-1, j+1] == 'S' and grid[i, j] == 'A' and grid[i+1, j-1] == 'M')

            # Down-right diagonal: (i+k, j+k)
            downright_mas = (grid[i-1, j-1] == 'M' and grid[i, j] == 'A' and grid[i+1, j+1] == 'S')
            downright_sam = (grid[i-1, j-1] == 'S' and grid[i, j] == 'A' and grid[i+1, j+1] == 'M')

            if (upright_mas or upright_sam) and (downright_mas or downright_sam):
                total += 1

    return total


test_string = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

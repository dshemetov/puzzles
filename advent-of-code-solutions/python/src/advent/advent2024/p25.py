"""25. https://adventofcode.com/2024/day/25"""

import numpy as np


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    3
    """
    s = s.strip("\n")

    schematics = s.split("\n\n")
    locks = []
    keys = []

    for schematic in schematics:
        grid = [list(line) for line in schematic.split("\n")]
        grid = np.array(grid)

        if grid[0, 0] == "#":
            lock_values = [np.where(grid[:, i] == ".")[0][0] - 1 for i in range(grid.shape[1])]
            locks.append(lock_values)
        else:
            key_values = [np.where(grid[:, i][::-1] == ".")[0][0] - 1 for i in range(grid.shape[1])]
            keys.append(key_values)

    total = 0
    for lock in locks:
        for key in keys:
            if all(l + k <= 5 for l, k in zip(lock, key)):
                total += 1

    return total


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    0
    """
    s = s.strip("\n")
    return 0


test_string = """
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
"""

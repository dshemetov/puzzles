# /// script
# requires-python = ">=3.14"
# dependencies = ["numpy"]
# ///
"""25. https://adventofcode.com/2024/day/25"""

import sys
import time

import numpy as np


def part_a(s: str) -> int:
    """
    Examples:
    >>> part_a(test_string)
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


def part_b(s: str) -> int:
    """
    Examples:
    >>> part_b(test_string)
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


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

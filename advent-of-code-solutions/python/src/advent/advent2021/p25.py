"""24. Sea Cucumber https://adventofcode.com/2021/day/25

Notes:

- A freebie after the last few.
"""

import numpy as np


def solve_a(s: str) -> str:
    cucumber_array = np.array([list(line.strip("\n")) for line in s.split("\n")])
    count = 0
    was_updated = True
    while was_updated:
        was_updated = False
        n, m = cucumber_array.shape
        for i, j in np.ndindex(n, m):
            if cucumber_array[i, j] == ">" and cucumber_array[i, (j + 1) % m] == ".":
                cucumber_array[i, (j + 1) % m] = ">"
                cucumber_array[i, j] = "."
                was_updated = True
            elif cucumber_array[i, j] == "v" and cucumber_array[(i + 1) % n, j] == ".":
                cucumber_array[(i + 1) % n, j] = "v"
                cucumber_array[i, j] = "."
                was_updated = True
        count += 1

    return count + 1


def solve_b(s: str) -> str:
    return 0

"""9. Mirage Maintenance https://adventofcode.com/2023/day/9"""

import numpy as np


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    114
    """
    nums = [np.array(x.split(), dtype=int) for x in s.strip("\n").splitlines()]
    total = 0
    for num in nums:
        diffs = [num]
        while not (diffs[-1] == 0).all():
            diffs.append(np.diff(diffs[-1]))
        s = 0
        for i in range(len(diffs)):
            s += diffs[i][-1]

        total += s

    return int(total)


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    2
    """
    nums = [np.array(x.split(), dtype=int) for x in s.strip("\n").splitlines()]
    total = 0
    for num in nums:
        diffs = [num]
        while not (diffs[-1] == 0).all():
            diffs.append(np.diff(diffs[-1]))
        s = 0
        for i in range(len(diffs) - 2, -1, -1):
            s = diffs[i][0] - s

        total += s

    return int(total)


test_string = """
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
"""

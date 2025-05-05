"""6. Wait For It https://adventofcode.com/2023/day/6

Notes:

- If the button is held for x seconds and the race time is t, the distance
  traveled is x * (t - x).
- Numpy doesn't make much of a difference speed-wise.
"""

import numpy as np


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    288
    """
    ts, ds = ([int(e) for e in x.split()[1:]] for x in s.strip("\n").split("\n"))
    win_counts = 1
    for t, d in zip(ts, ds):
        roots = np.roots([-1, t, -d])
        win_counts *= np.ceil(max(roots) - 1) - np.floor(min(roots) + 1) + 1
    return int(win_counts)


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    71503
    """
    t, d = (int("".join(x.split()[1:])) for x in s.strip("\n").split("\n"))
    roots = np.roots([-1, t, -d])
    win_counts = np.ceil(max(roots) - 1) - np.floor(min(roots) + 1) + 1
    return int(win_counts)


test_string = """
Time:      7  15   30
Distance:  9  40  200
"""

# /// script
# requires-python = ">=3.14"
# dependencies = ["numpy"]
# ///
"""6. Wait For It https://adventofcode.com/2023/day/6

Notes:

- If the button is held for x seconds and the race time is t, the distance
  traveled is x * (t - x).
- Numpy doesn't make much of a difference speed-wise.
"""

import numpy as np
import sys
import time


def part_a(s: str) -> int:
    ts, ds = ([int(e) for e in x.split()[1:]] for x in s.strip("\n").split("\n"))
    win_counts = 1
    for t, d in zip(ts, ds):
        roots = np.roots([-1, t, -d])
        win_counts *= np.ceil(max(roots) - 1) - np.floor(min(roots) + 1) + 1
    return int(win_counts)


def part_b(s: str) -> int:
    t, d = (int("".join(x.split()[1:])) for x in s.strip("\n").split("\n"))
    roots = np.roots([-1, t, -d])
    win_counts = np.ceil(max(roots) - 1) - np.floor(min(roots) + 1) + 1
    return int(win_counts)


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

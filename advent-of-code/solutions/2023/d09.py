# /// script
# requires-python = ">=3.14"
# dependencies = ["numpy"]
# ///
"""9. Mirage Maintenance https://adventofcode.com/2023/day/9"""

import numpy as np
import sys
import time


def part_a(s: str) -> int:
    """
    Examples:
    >>> part_a(test_string)
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


def part_b(s: str) -> int:
    """
    Examples:
    >>> part_b(test_string)
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


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

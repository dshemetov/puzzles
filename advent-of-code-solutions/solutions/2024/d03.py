# /// script
# requires-python = ">=3.14"
# dependencies = ["numpy"]
# ///
"""3. https://adventofcode.com/2024/day/3"""

import sys
import time
import re

import numpy as np


def part_a(s: str) -> int:
    """
    Examples:
    >>> part_a(test_string)
    161
    """
    s = s.strip("\n")
    matches = re.findall(r"mul\((\d+),(\d+)\)", s)
    if not matches:
        return 0
    data = np.array([[int(x), int(y)] for x, y in matches])
    return int(np.sum(data[:, 0] * data[:, 1]))


def part_b(s: str) -> int:
    """
    Examples:
    >>> part_b(test_string2)
    48
    """
    s = s.strip("\n")
    # Find do() and don't() positions
    doflags = [0] + [m.start() for m in re.finditer(r"do\(\)", s)]
    dontflags = [m.start() for m in re.finditer(r"don't\(\)", s)]

    # Find active parts of the string between do() and don't()
    active_ranges = []
    hi = 0
    for start in doflags:
        # Skip if already covered by previous range
        if active_ranges and active_ranges[-1][0] <= start <= active_ranges[-1][1]:
            continue

        while hi < len(dontflags) and dontflags[hi] < start:
            hi += 1

        if hi < len(dontflags):
            active_ranges.append((start, dontflags[hi]))
        else:
            active_ranges.append((start, len(s)))
            break

    # Extract valid substrings and find mul() expressions
    all_matches = []
    for start, end in active_ranges:
        matches = re.findall(r"mul\((\d+),(\d+)\)", s[start:end])
        all_matches.extend(matches)

    if not all_matches:
        return 0

    data = np.array([[int(x), int(y)] for x, y in all_matches])
    return int(np.sum(data[:, 0] * data[:, 1]))


test_string = """
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
"""
test_string2 = """
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

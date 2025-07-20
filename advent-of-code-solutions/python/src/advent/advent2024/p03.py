"""3. https://adventofcode.com/2024/day/3"""

import re

import numpy as np


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    161
    """
    s = s.strip("\n")
    matches = re.findall(r"mul\((\d+),(\d+)\)", s)
    if not matches:
        return 0
    data = np.array([[int(x), int(y)] for x, y in matches])
    return int(np.sum(data[:, 0] * data[:, 1]))


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string2)
    48
    """
    s = s.strip("\n")
    # Find do() and don't() positions like Julia
    doflags = [0] + [m.start() for m in re.finditer(r"do\(\)", s)]
    dontflags = [m.start() for m in re.finditer(r"don't\(\)", s)]

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

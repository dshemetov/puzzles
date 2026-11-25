# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Camp Cleanup
https://adventofcode.com/2022/day/4
"""

import sys
import time
import re


def part_a(s: str) -> int:
    """
    Examples:
    >>> part_a(test_string)
    4
    """
    s = s.strip("\n")
    total = 0
    for line in s.splitlines():
        a, b, c, d = [int(x) for x in re.findall(r"\d+", line)]
        if (a <= c <= d <= b) or (c <= a <= b <= d):
            total += 1
    return total


def part_b(s: str) -> int:
    """
    Examples:
    >>> part_b(test_string)
    6
    """
    s = s.strip("\n")
    total = 0
    for line in s.splitlines():
        a, b, c, d = [int(x) for x in re.findall(r"\d+", line)]
        if (a <= c <= b) or (c <= a <= d) or (a <= d <= b) or (c <= b <= d):
            total += 1
    return total


test_string = """
2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8
21-21,21-21
24-36,25-27
"""


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

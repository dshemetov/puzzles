# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Tuning Trouble
https://adventofcode.com/2022/day/6
"""

import sys
import time


def part_a(s: str) -> int:
    s = s.strip("\n")
    for i in range(4, len(s)):
        if len(set(s[i - 4 : i])) == 4:
            return i
    return -1


def part_b(s: str) -> int:
    s = s.strip("\n")
    for i in range(14, len(s)):
        if len(set(s[i - 14 : i])) == 14:
            return i
    return -1


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

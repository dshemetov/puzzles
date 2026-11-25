# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""https://adventofcode.com/2020/day/16"""

import sys
import time


def part_a(s: str) -> int:
    return 0


def part_b(s: str) -> int:
    return 0


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

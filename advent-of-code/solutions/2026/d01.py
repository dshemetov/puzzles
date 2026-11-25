# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""https://adventofcode.com/2026/day/1"""

import sys
import time

EXAMPLE = """\
"""


def parse(s: str):
    return s.strip("\n").splitlines()


def part_a(data) -> int:
    return 0


def part_b(data) -> int:
    return 0


if __name__ == "__main__":
    data = parse(open(sys.argv[1]).read())
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(data))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""https://adventofcode.com/2020/day/6"""

import sys
import time
from string import ascii_letters


def part_a(s: str) -> int:
    return sum(count_batch_union(batch) for batch in s.split("\n\n"))


def count_batch_union(s: str) -> int:
    return len(set().union(*(set(line.strip()) for line in s.split("\n"))))


def count_batch_intersection(s: str) -> int:
    return len(set(ascii_letters).intersection(*(set(line.strip()) for line in s.split("\n"))))


def part_b(s: str) -> int:
    return sum(count_batch_intersection(batch) for batch in s.split("\n\n"))


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

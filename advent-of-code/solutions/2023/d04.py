# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""4. Scratchcards https://adventofcode.com/2023/day/4"""

import sys
import time


def part_a(s: str) -> int:
    total = 0
    for line in s.strip("\n").splitlines():
        winning, have = line.split(":")[1].split("|")
        inter = len(set(winning.split()) & set(have.split()))
        total += 2 ** (inter - 1) if inter else 0

    return total


def part_b(s: str) -> int:
    lines = s.strip("\n").splitlines()
    copies = [1] * len(lines)
    for i, line in enumerate(lines):
        winning, have = line.split(":")[1].split("|")
        inter = len(set(winning.split()) & set(have.split()))
        upper_bound = min(i + 1 + inter, len(lines))
        copies[i + 1 : upper_bound] = [x + copies[i] for x in copies[i + 1 : upper_bound]]

    return sum(copies)


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

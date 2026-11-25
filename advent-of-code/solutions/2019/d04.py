# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Secure Container
https://adventofcode.com/2019/day/4
"""

import sys
import time


def part_a(s: str) -> int:
    a, b = [int(x) for x in s.split("-")]
    total = 0
    for i in range(a, b + 1):
        t = str(i)
        if not all(x <= y for x, y in zip(t, t[1:])):
            continue

        if not any(x == y for x, y in zip(t, t[1:])):
            continue

        total += 1
    return total


def part_b(s: str) -> int:
    a, b = [int(x) for x in s.split("-")]
    total = 0
    for i in range(a, b + 1):
        t = str(i)
        if not all(x <= y for x, y in zip(t, t[1:])):
            continue

        count = 0
        for j in range(0, 5):
            if t[j] == t[j + 1]:
                count += 1
            else:
                if count == 1:
                    total += 1
                    break
                count = 0
        else:
            if count == 1:
                total += 1

    return total


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

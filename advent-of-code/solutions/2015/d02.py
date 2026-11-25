# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""https://adventofcode.com/2015/day/2"""

import sys
import time


def part_a(s: str) -> int:
    b = s.split("\n")
    c = [i.split("x") for i in b]
    c.pop()
    return sum(
        [
            2 * (int(i[0]) * int(i[1]) + int(i[1]) * int(i[2]) + int(i[2]) * int(i[0]))
            + min(int(i[0]) * int(i[1]), int(i[1]) * int(i[2]), int(i[0]) * int(i[2]))
            for i in c
        ]
    )


def part_b(s: str) -> int:
    b = s.split("\n")
    c = [i.split("x") for i in b]
    c.pop()
    d = [[int(i[0]), int(i[1]), int(i[2])] for i in c]
    return sum(
        [i[0] * i[1] * i[2] + 2 * min(int(i[0]) + int(i[1]), int(i[1]) + int(i[2]), int(i[2]) + int(i[0])) for i in d]
    )


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

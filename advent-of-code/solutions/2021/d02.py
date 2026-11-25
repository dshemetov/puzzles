# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""2. Dive! https://adventofcode.com/2021/day/2"""

import sys
import time


def part_a(s: str) -> int:
    x, y = 0, 0
    for dir, n in (line.split(" ") for line in s.split("\n")):
        if dir == "forward":
            x += int(n)
        elif dir == "up":
            y += int(n)
        elif dir == "down":
            y -= int(n)
    return abs(x * y)


def part_b(s: str) -> int:
    x, y, aim = 0, 0, 0
    for dir, n in (line.split(" ") for line in s.split("\n")):
        if dir == "forward":
            x += int(n)
            y += aim * int(n)
        elif dir == "up":
            aim -= int(n)
        elif dir == "down":
            aim += int(n)
    return abs(x * y)


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

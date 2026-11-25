# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""2. Dive! https://adventofcode.com/2021/day/2"""

import sys
import time


def part_a(s: str) -> int:
    """
    Example:
    >>> part_a(test_string)
    150
    """
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
    """
    Example:
    >>> part_b(test_string)
    900
    """
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


test_string = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""2. Cube Conundrum https://adventofcode.com/2023/day/2"""

import re
import sys
import time
from math import prod


def part_a(s: str) -> int:
    s = s.strip("\n")
    r = re.compile(r"((?P<number>\d+) (?P<color>\w+))")
    total = 0
    for i, line in enumerate(s.splitlines(), 1):
        ok = True
        for m in r.finditer(line):
            if (
                (m.group("color") == "red" and int(m.group("number")) > 12)
                or (m.group("color") == "green" and int(m.group("number")) > 13)
                or (m.group("color") == "blue" and int(m.group("number")) > 14)
            ):
                ok = False
                break

        if ok:
            total += i

    return total


def part_b(s: str) -> int:
    s = s.strip("\n")
    r = re.compile(r"((?P<number>\d+) (?P<color>\w+))")
    total = 0
    for line in s.splitlines():
        maxes = {"red": 0, "green": 0, "blue": 0}
        for m in r.finditer(line):
            maxes[m.group("color")] = max(maxes[m.group("color")], int(m.group("number")))

        total += prod(maxes.values())

    return total


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

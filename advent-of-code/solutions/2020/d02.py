# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""https://adventofcode.com/2020/day/2"""

import sys
import time
import re


def part_a(s: str) -> int:
    lines = (m.groups() for m in re.finditer(r"(\d+)-(\d+) (\w): (\w+)", s))
    return sum(1 if int(cmin) <= password.count(char) <= int(cmax) else 0 for cmin, cmax, char, password in lines)


def part_b(s: str) -> int:
    lines = (m.groups() for m in re.finditer(r"(\d+)-(\d+) (\w): (\w+)", s))
    return sum(
        1 if (password[int(cmin) - 1] == char) ^ (password[int(cmax) - 1] == char) else 0
        for cmin, cmax, char, password in lines
    )


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

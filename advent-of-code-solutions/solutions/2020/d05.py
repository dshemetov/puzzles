# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""https://adventofcode.com/2020/day/5"""

import sys
import time


def part_a(s: str) -> int:
    return max(get_seatid(line) for line in s.split("\n"))


def get_seatid(s: str) -> int:
    return 8 * get_row(s[:7]) + get_col(s[7:])


def get_row(s: str) -> int:
    return int(s.replace("B", "1").replace("F", "0"), 2)


def get_col(s: str) -> int:
    return int(s.replace("R", "1").replace("L", "0"), 2)


def part_b(s: str) -> int:
    ids = set([get_seatid(line) for line in s.split("\n")])
    for x in ids:
        if x + 1 not in ids and x + 2 in ids:
            break
    return x + 1


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

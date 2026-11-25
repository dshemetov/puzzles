# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""12. Hot Springs https://adventofcode.com/2023/day/12"""

from functools import cache
import sys
import time


def part_a(s: str) -> int:
    s = s.strip("\n")
    lines = [line.split(" ") for line in s.splitlines()]
    rows = ((x, tuple(int(c) for c in y.split(","))) for x, y in lines)
    return sum(recurse(springs + ".", runs, 0) for springs, runs in rows)


@cache
def recurse(springs: str, runs: tuple[int], current_run: int) -> int:
    """
    Examples:
    >>> recurse("?.", (1,), 0)
    1
    >>> recurse("??.", (1,), 0)
    2
    >>> recurse("???.", (1,), 0)
    3
    >>> recurse("???.", (1, 1), 0)
    1
    >>> recurse("????.", (1, 1), 0)
    3
    >>> recurse("?????.", (1, 1), 0)
    6
    """
    # Get a point only if both springs and runs are exhausted. If runs is
    # exhausted, but springs isn't, then we keep recursing.
    if not springs:
        return not runs

    total = 0
    options = [".", "#"] if springs[0] == "?" else springs[0]
    for c in options:
        if c == "#":
            total += recurse(springs[1:], runs, current_run + 1)
        elif current_run:
            if runs and runs[0] == current_run:
                total += recurse(springs[1:], runs[1:], 0)
        else:
            total += recurse(springs[1:], runs, 0)
    return total


def part_b(s: str) -> int:
    rows = (
        (x, tuple(int(c) for c in y.split(","))) for x, y in (line.split(" ") for line in s.strip("\n").splitlines())
    )
    return sum(recurse("?".join([gears] * 5) + ".", code * 5, 0) for gears, code in rows)


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

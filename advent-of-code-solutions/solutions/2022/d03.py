# /// script
# requires-python = ">=3.14"
# dependencies = ["more-itertools"]
# ///
"""3. Rucksack Reorganization https://adventofcode.com/2022/day/3"""

import sys
import time
from string import ascii_lowercase, ascii_uppercase

from more_itertools import grouper

letters = ascii_lowercase + ascii_uppercase


def part_a(s: str) -> int:
    """
    Examples:
    >>> part_a(test_string)
    157
    """
    s = s.strip("\n")
    total = 0
    for line in s.splitlines():
        a = line[: len(line) // 2]
        b = line[len(line) // 2 :]
        c = (set(a) & set(b)).pop()
        total += letters.index(c) + 1
    return total


def part_b(s: str) -> int:
    """
    Examples:
    >>> part_b(test_string)
    70
    """
    s = s.strip("\n")
    total = 0
    for a, b, c in grouper(s.splitlines(), 3):
        d = (set(a) & set(b) & set(c)).pop()
        total += letters.index(d) + 1
    return total


test_string = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

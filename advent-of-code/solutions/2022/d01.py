# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""1. Calorie Counting https://adventofcode.com/2022/day/1"""

import sys
import time
from bisect import insort
from collections.abc import Iterable


def nlargest(n: int, it: Iterable) -> list:
    """
    Examples:
    >>> nlargest(5, [5, 4, 3, 10, 2, 5])
    [3, 4, 5, 5, 10]
    """
    top_n = []
    for e in it:
        insort(top_n, e)
        if len(top_n) > n:
            top_n.pop(0)
    return top_n


def part_a(s: str) -> int:
    """
    Examples:
    >>> part_a(test_string)
    24000
    """
    s = s.strip("\n")
    return max(sum(int(food) for food in elf.splitlines() if food.isnumeric()) for elf in s.split("\n\n"))


def part_b(s: str) -> int:
    """
    Examples:
    >>> part_b(test_string)
    45000
    """
    s = s.strip("\n")
    weight = (sum(int(food) for food in elf.splitlines() if food.isnumeric()) for elf in s.split("\n\n"))
    return sum(nlargest(3, weight))


test_string = """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

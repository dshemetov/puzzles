# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""The Tyranny of the Rocket Equation
https://adventofcode.com/2019/day/1

Fun fact: you can approximate the rocket equation in part b with x / 2 - 11.
This can be derived by ignoring the floor function and solving the recurrence relation for x.
"""

import sys
import time


def part_a(s: str) -> int:
    """
    Examples:
    >>> part_a(test_string)
    34241
    """
    s = [int(x) for x in s.strip("\n").split("\n")]
    return sum(x // 3 - 2 for x in s)


def part_b(s: str) -> int:
    """
    Examples:
    >>> part_b(test_string)
    51316
    """
    s = [int(x) for x in s.strip("\n").split("\n")]
    total = 0
    for x in s:
        while x > 0:
            x = x // 3 - 2
            if x > 0:
                total += x
    return total


test_string = """12
14
1969
100756
"""


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

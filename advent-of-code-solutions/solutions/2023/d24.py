# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""24. https://adventofcode.com/2023/day/24"""

import sys
import time

def part_a(s: str) -> int:
    """
    Examples:
    >>> part_a(test_string)
    0
    """
    s = s.strip("\n")
    return 0


def part_b(s: str) -> int:
    """
    Examples:
    >>> part_b(test_string)
    0
    """
    s = s.strip("\n")
    return 0


test_string = """
"""


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

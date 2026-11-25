# /// script
# requires-python = ">=3.14"
# dependencies = ["sympy"]
# ///
"""https://adventofcode.com/2020/day/10"""

import sys
import time
from collections.abc import Iterable
from functools import reduce
from itertools import chain, pairwise

from sympy import Poly, symbols


def part_a(s: str) -> int:
    nums = [int(line) for line in s.split("\n")]
    nums = [0] + sorted(nums) + [max(nums) + 3]
    diffs = [y - x for x, y in pairwise(nums)]
    return diffs.count(1) * diffs.count(3)


def part_b(s: str) -> int:
    # Get the sorted adapter sequence
    nums = [int(line) for line in s.split("\n")]
    nums = chain([0], sorted(nums), [max(nums) + 3])
    # Find the diffs, add a 3 at the beginning and end to cap off edge 1-sequences
    diffs = chain([3], diff(nums), [3])
    # Find the end points of the 1-sequences
    ixs = (i for i, x in enumerate(diffs) if x == 3)
    # The length of the 1-sequence [a, b] is (b - a - 1)
    diffs = (integer_composition(x - 1) for x in diff(ixs))
    return reduce(lambda x, y: x * y, diffs)


def diff(iterable: Iterable[int]) -> Iterable[int]:
    return (y - x for x, y in pairwise(iterable))


def integer_composition(n: int) -> int:
    x = symbols("x")
    f = 0
    for k in range(n + 1):
        f += (x + x**2 + x**3) ** k
    return int(Poly(f, x).coeff_monomial(x**n))


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""https://adventofcode.com/2015/day/4"""

import hashlib
import sys
import time


def mine(key: str, prefix: str) -> int:
    h = hashlib.new("md5")
    for i in range(10000000):
        h.update(f"{key}{i}".encode("ascii"))
        if h.hexdigest()[0 : len(prefix)] == prefix:
            break

    return i


def part_a(s: str) -> int:
    return mine(s.strip(), "00000")


def part_b(s: str) -> int:
    return mine(s.strip(), "000000")


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

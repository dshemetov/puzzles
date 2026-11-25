# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""https://adventofcode.com/2015/day/3"""

import sys
import time

def part_a(s: str) -> int:
    G = set()
    og = [0, 0]
    G.add(tuple(og))

    for m in s:
        if m == "^":
            og[1] += 1
            G.add(tuple(og))
        elif m == "v":
            og[1] -= 1
            G.add(tuple(og))
        elif m == "<":
            og[0] -= 1
            G.add(tuple(og))
        else:
            og[0] += 1
            G.add(tuple(og))

    return len(G)


def part_b(s: str) -> int:
    G1 = set()
    G2 = set()
    og1 = [0, 0]
    og2 = [0, 0]
    G1.add(tuple(og1))
    G2.add(tuple(og2))

    i = 1
    for m in s:
        if m == "^":
            if i % 2 == 0:
                og1[1] += 1
                G1.add(tuple(og1))
            else:
                og2[1] += 1
                G2.add(tuple(og2))
        elif m == "v":
            if i % 2 == 0:
                og1[1] -= 1
                G1.add(tuple(og1))
            else:
                og2[1] -= 1
                G2.add(tuple(og2))
        elif m == "<":
            if i % 2 == 0:
                og1[0] -= 1
                G1.add(tuple(og1))
            else:
                og2[0] -= 1
                G2.add(tuple(og2))
        else:
            if i % 2 == 0:
                og1[0] += 1
                G1.add(tuple(og1))
            else:
                og2[0] += 1
                G2.add(tuple(og2))
        i += 1

    return len(G1.union(G2))


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

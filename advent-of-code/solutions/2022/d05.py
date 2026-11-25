# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Supply Stacks
https://adventofcode.com/2022/day/5
"""

import sys
import time
import re
from collections import defaultdict, deque


def part_a(s: str) -> str:
    s = s.strip("\n")
    s1, s2 = s.split("\n\n")
    s1 = s1.split("\n")
    s2 = s2.split("\n")

    stacks = defaultdict(deque)
    r = re.compile(r"([A-Z])")
    for line in s1:
        for m in r.finditer(line):
            # Each stack is 4 characters wide
            stacks[(m.start() - 1) // 4 + 1].appendleft(m.group())

    r = re.compile(r"move (\d+) from (\d+) to (\d+)")
    for line in s2:
        if not line:
            continue
        num, f, t = r.findall(line)[0]
        num, f, t = int(num), int(f), int(t)
        for _ in range(num):
            stacks[t].append(stacks[f].pop())

    return "".join(stacks[key][-1] for key in sorted(stacks.keys()))


def part_b(s: str) -> str:
    s = s.strip("\n")
    s1, s2 = s.split("\n\n")
    s1 = s1.split("\n")
    s2 = s2.split("\n")

    stacks = defaultdict(deque)
    r = re.compile(r"([A-Z])")
    for line in s1:
        for m in r.finditer(line):
            # Each stack is 4 characters wide
            stacks[(m.start() - 1) // 4 + 1].appendleft(m.group())

    r = re.compile(r"move (\d+) from (\d+) to (\d+)")
    for line in s2:
        if not line:
            continue
        num, f, t = r.findall(line)[0]
        num, f, t = int(num), int(f), int(t)

        stacks[t].extend(list(stacks[f])[-num:])

        for _ in range(num):
            stacks[f].pop()

    return "".join(stacks[key][-1] for key in sorted(stacks.keys()))


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

"""Supply Stacks
https://adventofcode.com/2022/day/5
"""

import re
from collections import defaultdict, deque


def solve_a(s: str) -> str:
    """
    Examples:
    >>> solve_a(test_string)
    'CMZ'
    """
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


def solve_b(s: str) -> str:
    """
    Examples:
    >>> solve_b(test_string)
    'MCD'
    """
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


test_string = """
    [D]
[N] [C]
[Z] [M] [P]
 1   2   3

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
"""

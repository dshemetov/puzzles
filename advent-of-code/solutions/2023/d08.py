# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""8. Haunted Wasteland https://adventofcode.com/2023/day/8

Part a is a simple binary tree traversal. I'm not a big fan of part b, since the
solution depends on noticing that the data contains hidden assumptions not
stated in the problem. Namely each traversal of the binary tree is cyclical,
where the length of the period is exactly equal to the time it takes to
encounter the first "Z" node. This allows us to find the cycle intersection
using least common multiples. Otherwise, the problem would've been a linear
Diophantine equation and would have required the Chinese Remainder Theorem.
"""

import re
from itertools import cycle
from math import lcm
import sys
import time


def part_a(s: str) -> int:
    commands, *network = s.strip("\n").splitlines()

    d = {}
    for node in network[1:]:
        node, *children = re.findall(r"\w+", node)
        d[node] = children

    cur_node = "AAA"
    for i, command in enumerate(cycle(commands)):
        if cur_node == "ZZZ":
            return i
        cur_node = d[cur_node][command == "R"]

    return -1


def part_b(s: str) -> int:
    """
    Examples:
    >>> part_b(test_string3)
    6
    """
    """
    Examples:
    >>> part_b(get_puzzle_input(2023, 8))
    """
    commands, *network = s.strip("\n").splitlines()

    d = {}
    for node in network[1:]:
        node, *children = re.findall(r"\w+", node)
        d[node] = children

    start_nodes = [x for x in d if x.endswith("A")]
    paths = []
    lengths = []
    for start_node in start_nodes:
        cur_node = start_node
        seen = set()
        path = []
        for j, command in cycle(enumerate(commands)):
            if (cur_node, j) in seen:
                break
            path.append((cur_node, j))
            seen |= {(cur_node, j)}
            cur_node = d[cur_node][command == "R"]
        path.append((cur_node, j))
        lengths.append(len(path) - 1 - path.index(path[-1]))
        paths.append(path)

    return lcm(*lengths)


test_string3 = """
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
"""


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Passage Pathing
https://adventofcode.com/2021/day/12
"""

import sys
import time
from collections import defaultdict

Path = list[str]
Graph = dict[str, list[str]]


def part_a(s: str) -> int:
    return len(get_paths(parse_input(s)))


def parse_input(s: str) -> Graph:
    node_map = defaultdict(list)
    for line in s.split("\n"):
        s, t = line.split("-")
        node_map[s].append(t)
        node_map[t].append(s)
    return node_map


def get_paths(node_map: Graph, part: str = "a") -> list[Path]:
    finished_paths = []
    unfinished_paths = [["start"]]
    while len(unfinished_paths) > 0:
        path = unfinished_paths.pop()
        for node in get_valid_steps(path, node_map, part):
            if node == "start":
                continue
            new_path = path.copy()
            new_path.append(node)
            if node == "end":
                finished_paths.append(new_path)
            else:
                unfinished_paths.append(new_path)
    return finished_paths


def get_valid_steps(path: Path, node_map: dict, part: str) -> list[str]:
    if part == "a":
        return (
            option for option in node_map[path[-1]] if option.isupper() or (option.islower() and option not in path)
        )
    if part == "b":
        exists_small_cave_double_visit = any(path.count(x) > 1 for x in path if x.islower())
        if exists_small_cave_double_visit:
            return (
                option for option in node_map[path[-1]] if option.isupper() or (option.islower() and option not in path)
            )
        else:
            return (
                option
                for option in node_map[path[-1]]
                if option.isupper() or (option.islower() and path.count(option) < 2)
            )
    raise ValueError("Not implemented.")


def part_b(s: str) -> int:
    return len(get_paths(parse_input(s), part="b"))


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

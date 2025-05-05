"""Passage Pathing
https://adventofcode.com/2021/day/12
"""

from collections import defaultdict

Path = list[str]
Graph = dict[str, list[str]]


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_strings[0])
    10
    >>> solve_a(test_strings[1])
    19
    >>> solve_a(test_strings[2])
    226
    """
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


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_strings[0])
    36
    >>> solve_b(test_strings[1])
    103
    >>> solve_b(test_strings[2])
    3509
    """
    return len(get_paths(parse_input(s), part="b"))


test_strings = [
    """start-A
start-b
A-c
A-b
b-d
A-end
b-end""",
    """dc-end
HN-start
start-kj
dc-start
dc-HN
LN-dc
HN-end
kj-sa
kj-HN
kj-dc""",
    """fs-end
he-DX
fs-he
start-DX
pj-DX
end-zg
zg-sl
zg-pj
pj-he
RW-he
fs-DX
pj-RW
zg-RW
start-pj
he-WI
zg-he
pj-fs
start-RW""",
]

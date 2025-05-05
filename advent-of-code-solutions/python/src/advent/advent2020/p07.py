"""Handy Haversacks
https://adventofcode.com/2020/day/7
"""

import re


def solve_a(s: str) -> int:
    d = dict([parse_line(line) for line in s.split("\n")])
    traversed = set()
    to_traverse = set(["shiny gold"])
    while len(to_traverse) > 0:
        entry = to_traverse.pop()
        traversed.add(entry)
        parents = get_parents(entry, d)
        to_traverse |= set(parents) - traversed
    return len(traversed) - 1


def parse_line(line: str) -> tuple[str, str]:
    """
    Examples:
    >>> parse_line(
    ...     "light salmon bags contain 5 wavy plum bags, 4 drab white bags, 5 muted bronze bags, 5 mirrored beige bags."
    ... )
    ('light salmon', [[5, 'wavy plum'], [4, 'drab white'], [5, 'muted bronze'], [5, 'mirrored beige']])
    """
    container_bag, contained_bags = re.match(r"(\w+ \w+) bags contain (.*)", line).groups()
    contained_bags = [
        [int(e.groups()[0]), e.groups()[1]] for e in re.finditer(r"(\d+) (\w+ \w+) bags?", contained_bags)
    ]
    return (container_bag, contained_bags)


def get_parents(child, d):
    return [e for e in d if child in flatten(d[e])]


def flatten(lst: list[list]) -> list:
    return [e for row in lst for e in row]


def solve_b(s: str) -> int:
    d = dict([parse_line(line) for line in s.split("\n")])
    return get_bags(d, "shiny gold") - 1


def get_bags(d, e):
    n = sum(bag[0] * get_bags(d, bag[1]) for bag in d[e]) if len(d[e]) > 0 else 0
    return n + 1


test_input = """shiny gold bags contain 2 dark red bags.
dark red bags contain 2 dark orange bags.
dark orange bags contain 2 dark yellow bags.
dark yellow bags contain 2 dark green bags.
dark green bags contain 2 dark blue bags.
dark blue bags contain 2 dark violet bags.
dark violet bags contain no other bags."""

"""2. Cube Conundrum https://adventofcode.com/2023/day/2"""

import re
from math import prod


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    8
    """
    s = s.strip("\n")
    r = re.compile(r"((?P<number>\d+) (?P<color>\w+))")
    total = 0
    for i, line in enumerate(s.splitlines(), 1):
        ok = True
        for m in r.finditer(line):
            if (
                (m.group("color") == "red" and int(m.group("number")) > 12)
                or (m.group("color") == "green" and int(m.group("number")) > 13)
                or (m.group("color") == "blue" and int(m.group("number")) > 14)
            ):
                ok = False
                break

        if ok:
            total += i

    return total


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    2286
    """
    s = s.strip("\n")
    r = re.compile(r"((?P<number>\d+) (?P<color>\w+))")
    total = 0
    for line in s.splitlines():
        maxes = {"red": 0, "green": 0, "blue": 0}
        for m in r.finditer(line):
            maxes[m.group("color")] = max(maxes[m.group("color")], int(m.group("number")))

        total += prod(maxes.values())

    return total


test_string = """
Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green
Game 2: 1 blue, 2 green; 3 green, 4 blue, 1 red; 1 green, 1 blue
Game 3: 8 green, 6 blue, 20 red; 5 blue, 4 red, 13 green; 5 green, 1 red
Game 4: 1 green, 3 red, 6 blue; 3 green, 6 red; 3 green, 15 blue, 14 red
Game 5: 6 red, 1 blue, 3 green; 2 blue, 1 red, 2 green
"""

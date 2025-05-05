"""3. Rucksack Reorganization https://adventofcode.com/2022/day/3"""

from string import ascii_lowercase, ascii_uppercase

from more_itertools import grouper

letters = ascii_lowercase + ascii_uppercase


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    157
    """
    s = s.strip("\n")
    total = 0
    for line in s.splitlines():
        a = line[: len(line) // 2]
        b = line[len(line) // 2 :]
        c = (set(a) & set(b)).pop()
        total += letters.index(c) + 1
    return total


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    70
    """
    s = s.strip("\n")
    total = 0
    for a, b, c in grouper(s.splitlines(), 3):
        d = (set(a) & set(b) & set(c)).pop()
        total += letters.index(d) + 1
    return total


test_string = """
vJrwpWtwJgWrhcsFMMfFFhFp
jqHRNqRjqzjGDLGLrsFMfFZSrLrFZsSL
PmmdzqPrVvPwwTWBwg
wMqvLMZHhHMvwLHjbvcjnnSBnvTQFn
ttgJtRGJQctTZtZT
CrZsJsPPZsGzwwsLwLmpwMDw
"""

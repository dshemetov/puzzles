"""7. https://adventofcode.com/2024/day/7

Initial approach was using itertools.product, stopping early once I found one
solution. Took 5s though. Got the recursive idea from julienc91 on Reddit, so I
implemented it iteratively, which runs in 1s. Good enough!

https://www.reddit.com/r/adventofcode/comments/1h8l3z5/2024_day_7_solutions/m0ubb4e/
"""

import re
from collections import deque


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    3749
    """
    s = s.strip("\n")
    lines = [[int(x) for x in re.findall(r"\d+", x)] for x in s.splitlines()]

    total = 0
    for line in lines:
        if is_valid_iterative((line[0], tuple(line[1:])), False):
            total += line[0]

    return total


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    11387
    """
    s = s.strip("\n")
    lines = [[int(x) for x in re.findall(r"\d+", x)] for x in s.splitlines()]

    total = 0
    for line in lines:
        if is_valid_iterative((line[0], tuple(line[1:])), True):
            total += line[0]

    return total


def is_valid_iterative(equation: tuple[int, tuple[int, ...]], with_combination: bool) -> bool:
    stack = deque([equation])
    while stack:
        current_total, current_numbers = stack.pop()

        if len(current_numbers) == 1:
            if current_total == current_numbers[0]:
                return True
            continue

        a, b, *r = current_numbers

        if current_total < a:
            continue

        stack.append((current_total, (a + b, *r)))
        stack.append((current_total, (a * b, *r)))

        if with_combination:
            stack.append((current_total, (a * 10 ** len(str(b)) + b, *r)))

    return False


test_string = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

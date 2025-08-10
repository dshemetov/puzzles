"""7. https://adventofcode.com/2024/day/7"""

import re


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
        if backtrack(line[0], len(line[1:]) - 1, line[1:], False):
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
        if backtrack(line[0], len(line[1:]) - 1, line[1:], True):
            total += line[0]

    return total


def backtrack(target: int, idx: int, numbers: list[int], with_combination: bool) -> bool:
    if idx == 0:
        return target == numbers[0]

    current_num = numbers[idx]

    # Reverse addition
    if target > current_num and backtrack(target - current_num, idx - 1, numbers, with_combination):
        return True

    # Reverse multiplication
    if target % current_num == 0 and backtrack(target // current_num, idx - 1, numbers, with_combination):
        return True

    # Reverse concatenation
    if with_combination:
        num_str = str(current_num)
        target_str = str(target)
        if len(target_str) > len(num_str) and target_str.endswith(num_str):
            new_target_str = target_str[: -len(num_str)]
            if new_target_str:
                new_target = int(new_target_str)
                if backtrack(new_target, idx - 1, numbers, with_combination):
                    return True

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

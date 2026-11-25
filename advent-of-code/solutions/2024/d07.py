# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""7. https://adventofcode.com/2024/day/7"""

import re
import sys
import time


def part_a(s: str) -> int:
    s = s.strip("\n")
    lines = [[int(x) for x in re.findall(r"\d+", x)] for x in s.splitlines()]

    total = 0
    for line in lines:
        if backtrack(line[0], len(line[1:]) - 1, line[1:], False):
            total += line[0]

    return total


def part_b(s: str) -> int:
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


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

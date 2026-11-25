# /// script
# requires-python = ">=3.14"
# dependencies = ["numpy"]
# ///
"""5. https://adventofcode.com/2024/day/5"""

import sys
import time

import numpy as np


def part_a(s: str) -> int:
    s = s.strip("\n")
    rules_str, updates_str = s.split("\n\n")
    rules_lines = [line.split("|") for line in rules_str.splitlines()]
    rules_nums = np.array([[int(x) for x in line] for line in rules_lines])
    max_val = np.max(rules_nums)

    # Create BitMatrix for O(1) lookups
    rules_matrix = np.zeros((max_val + 1, max_val + 1), dtype=bool)
    rules_matrix[rules_nums[:, 0], rules_nums[:, 1]] = True

    # Parse updates to integers
    updates = [[int(x) for x in line.split(",")] for line in updates_str.splitlines()]

    total = 0
    for update in updates:
        valid = True
        for i in range(len(update)):
            for j in range(i + 1, len(update)):
                if not rules_matrix[update[i], update[j]]:
                    valid = False
                    break
            if not valid:
                break
        if valid:
            total += update[len(update) // 2]

    return total


def part_b(s: str) -> int:
    s = s.strip("\n")
    rules_str, updates_str = s.split("\n\n")
    rules_lines = [line.split("|") for line in rules_str.splitlines()]
    rules_nums = np.array([[int(x) for x in line] for line in rules_lines])
    max_val = np.max(rules_nums)

    # Create BitMatrix for O(1) lookups
    rules_matrix = np.zeros((max_val + 1, max_val + 1), dtype=bool)
    rules_matrix[rules_nums[:, 0], rules_nums[:, 1]] = True

    # Parse updates to integers
    updates = [[int(x) for x in line.split(",")] for line in updates_str.splitlines()]

    # Find invalid updates
    invalid = []
    for update in updates:
        valid = True
        for i in range(len(update)):
            for j in range(i + 1, len(update)):
                if not rules_matrix[update[i], update[j]]:
                    valid = False
                    break
            if not valid:
                break
        if not valid:
            invalid.append(update)

    # Fix invalid updates
    total = 0
    for update in invalid:
        for i in range(len(update)):
            for j in range(i + 1, len(update)):
                if rules_matrix[update[j], update[i]]:
                    update[i], update[j] = update[j], update[i]
        total += update[len(update) // 2]

    return total


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

"""5. https://adventofcode.com/2024/day/5"""

import numpy as np


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    143
    """
    s = s.strip("\n")
    rules_str, updates_str = s.split("\n\n")

    # Parse rules into matrix like Julia
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


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    123
    """
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


test_string = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

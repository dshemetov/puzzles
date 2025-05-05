"""5. https://adventofcode.com/2024/day/5"""


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    143
    """
    s = s.strip("\n")
    rules, updates = s.split("\n\n")
    rules = {tuple(x.split("|")) for x in rules.splitlines()}
    updates = [x.split(",") for x in updates.splitlines()]

    total = 0
    for update in updates:
        valid = True
        for i in range(len(update)):
            for j in range(i + 1, len(update)):
                if (update[j], update[i]) in rules:
                    valid = False
                    break
            if not valid:
                break
        if valid:
            total += int(update[len(update) // 2])

    return total


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    123
    """
    s = s.strip("\n")
    rules, updates = s.split("\n\n")
    rules = {tuple(x.split("|")) for x in rules.splitlines()}
    updates = [x.split(",") for x in updates.splitlines()]

    invalid = []
    for update in updates:
        valid = True
        for i in range(len(update)):
            for j in range(i + 1, len(update)):
                if (update[j], update[i]) in rules:
                    valid = False
                    break
            if not valid:
                break
        if not valid:
            invalid.append(update)

    total = 0
    for update in invalid:
        for i in range(len(update)):
            for j in range(i + 1, len(update)):
                if (update[j], update[i]) in rules:
                    update[i], update[j] = update[j], update[i]
        total += int(update[len(update) // 2])

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

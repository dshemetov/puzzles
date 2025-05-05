"""4. Scratchcards https://adventofcode.com/2023/day/4"""


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    13
    """
    total = 0
    for line in s.strip("\n").splitlines():
        winning, have = line.split(":")[1].split("|")
        inter = len(set(winning.split()) & set(have.split()))
        total += 2 ** (inter - 1) if inter else 0

    return total


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    30
    """
    lines = s.strip("\n").splitlines()
    copies = [1] * len(lines)
    for i, line in enumerate(lines):
        winning, have = line.split(":")[1].split("|")
        inter = len(set(winning.split()) & set(have.split()))
        upper_bound = min(i + 1 + inter, len(lines))
        copies[i + 1 : upper_bound] = [x + copies[i] for x in copies[i + 1 : upper_bound]]

    return sum(copies)


test_string = """
Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11
"""

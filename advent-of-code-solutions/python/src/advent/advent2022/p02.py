"""2. Rock Paper Scissors https://adventofcode.com/2022/day/2"""


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    15
    """
    s = s.strip("\n")
    total = 0
    for line in s.splitlines():
        match line.split():
            case "A", "X":
                total += 3 + 1
            case "A", "Y":
                total += 6 + 2
            case "A", "Z":
                total += 0 + 3
            case "B", "X":
                total += 0 + 1
            case "B", "Y":
                total += 3 + 2
            case "B", "Z":
                total += 6 + 3
            case "C", "X":
                total += 6 + 1
            case "C", "Y":
                total += 0 + 2
            case "C", "Z":
                total += 3 + 3

    return total


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    12
    """
    s = s.strip("\n")
    total = 0
    for line in s.splitlines():
        match line.split():
            case "A", "X":
                total += 0 + 3
            case "A", "Y":
                total += 3 + 1
            case "A", "Z":
                total += 6 + 2
            case "B", "X":
                total += 0 + 1
            case "B", "Y":
                total += 3 + 2
            case "B", "Z":
                total += 6 + 3
            case "C", "X":
                total += 0 + 2
            case "C", "Y":
                total += 3 + 3
            case "C", "Z":
                total += 6 + 1

    return total


test_string = """
A Y
B X
C Z
"""

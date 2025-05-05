"""Secure Container
https://adventofcode.com/2019/day/4
"""


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    10
    """
    a, b = [int(x) for x in s.split("-")]
    total = 0
    for i in range(a, b + 1):
        t = str(i)
        if not all(x <= y for x, y in zip(t, t[1:])):
            continue

        if not any(x == y for x, y in zip(t, t[1:])):
            continue

        total += 1
    return total


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    1
    """
    a, b = [int(x) for x in s.split("-")]
    total = 0
    for i in range(a, b + 1):
        t = str(i)
        if not all(x <= y for x, y in zip(t, t[1:])):
            continue

        count = 0
        for j in range(0, 5):
            if t[j] == t[j + 1]:
                count += 1
            else:
                if count == 1:
                    total += 1
                    break
                count = 0
        else:
            if count == 1:
                total += 1

    return total


test_string = """111111-111122"""

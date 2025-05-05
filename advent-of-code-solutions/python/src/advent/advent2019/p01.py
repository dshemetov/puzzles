"""The Tyranny of the Rocket Equation
https://adventofcode.com/2019/day/1

Fun fact: you can approximate the rocket equation in part b with x / 2 - 11.
This can be derived by ignoring the floor function and solving the recurrence relation for x.
"""


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    34241
    """
    s = [int(x) for x in s.strip("\n").split("\n")]
    return sum(x // 3 - 2 for x in s)


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    51316
    """
    s = [int(x) for x in s.strip("\n").split("\n")]
    total = 0
    for x in s:
        while x > 0:
            x = x // 3 - 2
            if x > 0:
                total += x
    return total


test_string = """12
14
1969
100756
"""

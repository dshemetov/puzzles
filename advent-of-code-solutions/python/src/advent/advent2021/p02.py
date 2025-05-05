"""2. Dive! https://adventofcode.com/2021/day/2"""


def solve_a(s: str) -> int:
    """
    Example:
    >>> solve_a(test_string)
    150
    """
    x, y = 0, 0
    for dir, n in (line.split(" ") for line in s.split("\n")):
        if dir == "forward":
            x += int(n)
        elif dir == "up":
            y += int(n)
        elif dir == "down":
            y -= int(n)
    return abs(x * y)


def solve_b(s: str) -> int:
    """
    Example:
    >>> solve_b(test_string)
    900
    """
    x, y, aim = 0, 0, 0
    for dir, n in (line.split(" ") for line in s.split("\n")):
        if dir == "forward":
            x += int(n)
            y += aim * int(n)
        elif dir == "up":
            aim -= int(n)
        elif dir == "down":
            aim += int(n)
    return abs(x * y)


test_string = """forward 5
down 5
forward 8
up 3
down 8
forward 2"""

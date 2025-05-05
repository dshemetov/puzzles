"""1. Calorie Counting https://adventofcode.com/2022/day/1"""

from advent.tools import nlargest


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    24000
    """
    s = s.strip("\n")
    return max(sum(int(food) for food in elf.splitlines() if food.isnumeric()) for elf in s.split("\n\n"))


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    45000
    """
    s = s.strip("\n")
    weight = (sum(int(food) for food in elf.splitlines() if food.isnumeric()) for elf in s.split("\n\n"))
    return sum(nlargest(3, weight))


test_string = """
1000
2000
3000

4000

5000
6000

7000
8000
9000

10000
"""

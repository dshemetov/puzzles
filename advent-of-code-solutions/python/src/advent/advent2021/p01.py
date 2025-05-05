"""1. Sonar Sweep https://adventofcode.com/2021/day/1"""


def solve_a(s: str) -> int:
    """
    Example:
    >>> solve_a(test_string)
    7
    """
    nums = [int(x) for x in s.split("\n")]
    return sum(1 if y > x else 0 for x, y in zip(nums[:-1], nums[1:]))


def solve_b(s: str) -> int:
    """
    Example:
    >>> solve_b(test_string)
    5
    """
    nums = [int(x) for x in s.split("\n")]
    windowed_sums = [sum(triple) for triple in zip(nums[:-2], nums[1:-1], nums[2:])]
    return sum(1 if y > x else 0 for x, y in zip(windowed_sums[:-1], windowed_sums[1:]))


test_string = """199
200
208
210
200
207
240
269
260
263"""

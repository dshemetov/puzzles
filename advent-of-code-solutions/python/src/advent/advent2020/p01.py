from itertools import combinations


def solve_a(s: str) -> int:
    nums = [int(n) for n in s.split("\n")]
    return next(x * y for x, y in combinations(nums, 2) if x + y == 2020)


def solve_b(s: str) -> int:
    nums = [int(n) for n in s.split("\n")]
    return next(x * y * z for x, y, z in combinations(nums, 3) if x + y + z == 2020)

"""14. https://adventofcode.com/2024/day/14"""

import re

import numpy as np
from numba import int64, njit


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    12
    """
    lines = s.strip().split("\n")
    nums = []

    for line in lines:
        matches = re.findall(r"-?\d+", line)
        nums.append([int(x) for x in matches])
    nums = np.array(nums, dtype=np.int64)  # n x 4

    if len(lines) <= 12:  # Test case
        width, height = 11, 7
    else:  # Real input
        width, height = 101, 103

    return solve_a_core(nums, width, height)


@njit(int64(int64[:, :], int64, int64), cache=True)
def get_score(nums: np.ndarray, width: int, height: int) -> int:
    quadrants = [0, 0, 0, 0]
    mid_x, mid_y = width // 2, height // 2

    for i in range(len(nums)):
        x, y = nums[i, 0], nums[i, 1]
        if x < mid_x and y < mid_y:
            quadrants[0] += 1
        elif x < mid_x and y > mid_y:
            quadrants[1] += 1
        elif x > mid_x and y < mid_y:
            quadrants[2] += 1
        elif x > mid_x and y > mid_y:
            quadrants[3] += 1

    return quadrants[0] * quadrants[1] * quadrants[2] * quadrants[3]


@njit(int64(int64[:, :], int64, int64), cache=True)
def solve_a_core(nums: np.ndarray, width: int, height: int) -> int:
    for _ in range(100):
        nums[:, 0] = (nums[:, 0] + nums[:, 2]) % width
        nums[:, 1] = (nums[:, 1] + nums[:, 3]) % height

    return get_score(nums, width, height)


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    1
    """
    lines = s.strip().split("\n")
    nums = []
    for line in lines:
        matches = re.findall(r"-?\d+", line)
        nums.append([int(x) for x in matches])
    nums = np.array(nums, dtype=np.int64)  # n x 4

    if len(lines) <= 12:  # Test case
        width, height = 11, 7
    else:  # Real input
        width, height = 101, 103

    return solve_b_core(nums, width, height)


@njit(int64(int64[:, :], int64, int64), cache=True)
def check_cluster(nums: np.ndarray, width: int, height: int) -> int:
    """Check how many robots are clustered near the center."""
    mid_x, mid_y = width // 2, height // 2

    count = 0
    for i in range(len(nums)):
        x, y = nums[i, 0], nums[i, 1]
        if mid_x - 5 <= x <= mid_x + 5 and mid_y - 5 <= y <= mid_y + 5:
            count += 1

    return -count  # Negative because we want to minimize this


@njit(int64(int64[:, :], int64, int64), cache=True)
def solve_b_core(nums: np.ndarray, width: int, height: int) -> int:
    smallest_score = float("inf")
    step_of_smallest_score = 0

    for i in range(1, 10001):
        nums[:, 0] = (nums[:, 0] + nums[:, 2]) % width
        nums[:, 1] = (nums[:, 1] + nums[:, 3]) % height

        score = check_cluster(nums, width, height)

        if score < smallest_score:
            smallest_score = score
            step_of_smallest_score = i

    return step_of_smallest_score


test_string = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""

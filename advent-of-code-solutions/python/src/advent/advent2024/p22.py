"""22. https://adventofcode.com/2024/day/22"""

import numpy as np
from numba import int64, njit


@njit(int64(int64), cache=True)
def next_num(n: int) -> int:
    prune_mask = (1 << 24) - 1
    n = ((n << 6) ^ n) & prune_mask
    n = ((n >> 5) ^ n) & prune_mask
    n = ((n << 11) ^ n) & prune_mask
    return n


@njit(int64(int64[:], int64, int64), cache=True)
def solve_a_core(nums: np.ndarray, n: int, m: int) -> int:
    total = 0
    for i in range(m):
        sn = nums[i]
        for _ in range(n):
            sn = next_num(sn)
        total += sn
    return total


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string_a)
    37327623
    """
    s = s.strip("\n")
    nums = np.array(s.splitlines(), dtype=np.int64)
    n, m = 2000, len(nums)
    return solve_a_core(nums, n, m)


@njit(int64(int64[:], int64, int64), cache=True)
def solve_b_core(nums: np.ndarray, n: int, m: int) -> int:
    # Get prices for each monkey
    ps = np.zeros((n + 1, m), dtype=np.int64)
    for i, sn in enumerate(nums):
        ps[0][i] = sn % 10
        for j in range(n):
            sn = next_num(sn)
            ps[j + 1][i] = sn % 10

    # Get price changes for each monkey. Range is [-9, 9], so shift up by 9 to
    # avoid negative indices.
    pds = np.zeros((n, m), dtype=np.int64)
    for i in range(m):
        for j in range(n):
            pds[j][i] = ps[j + 1][i] - ps[j][i] + 9

    # Scan through each monkey's price changes, creating 4-digit prefixes, and
    # tallying the profits for each prefix.
    prefix_profits = np.zeros(19**4, dtype=np.int64)
    for i in range(m):
        seen = np.zeros(19**4, dtype=np.bool_)
        for j in range(n - 3):
            index = pds[j][i] * 19**3 + pds[j + 1][i] * 19**2 + pds[j + 2][i] * 19 + pds[j + 3][i]
            # Only the first occurrence matters.
            if not seen[index]:
                # pds[j+3][i] = ps[j+4][i] - ps[j+3][i]
                # so ps[j+4][i] is the current price.
                prefix_profits[index] += ps[j + 4][i]
                seen[index] = True

    return max(prefix_profits)


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string_b)
    23
    """
    s = s.strip("\n")
    nums = np.array(s.splitlines(), dtype=np.int64)
    n, m = 2000, len(nums)
    return solve_b_core(nums, n, m)


test_string_a = """
1
10
100
2024
"""

test_string_b = """
1
2
3
2024
"""

"""Binary Diagnostics
https://adventofcode.com/2021/day/3
"""

from copy import copy

import numpy as np

from advent.tools import binary_to_int


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    198
    """
    mat = np.array([list(line) for line in s.strip("\n").split("\n")], dtype=int)
    n, _ = mat.shape
    max_rows = mat.sum(axis=0) >= n / 2
    min_rows = ~max_rows
    max_rows = max_rows.astype(int)
    min_rows = min_rows.astype(int)
    gamma_rate, epsilon_rate = binary_to_int(max_rows), binary_to_int(min_rows)
    return gamma_rate * epsilon_rate


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    230
    """
    mat = np.array([list(line) for line in s.strip("\n").split("\n")], dtype=int)
    _, m = mat.shape

    mat_ = copy(mat)
    for ix in range(m):
        if len(mat_) == 1:
            break
        n, _ = mat_.shape
        mat_ = mat_[mat_[:, ix] == int(mat_[:, ix].sum() >= n / 2)]
    oxygen_rating = binary_to_int(mat_[0])

    mat_ = copy(mat)
    for ix in range(m):
        if len(mat_) == 1:
            break
        n, _ = mat_.shape
        mat_ = mat_[mat_[:, ix] == int(mat_[:, ix].sum() < n / 2)]
    co2_rating = binary_to_int(mat_[0])

    return oxygen_rating * co2_rating


test_string = """
00100
11110
10110
10111
10101
01111
00111
11100
10000
11001
00010
01010
"""

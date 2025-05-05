"""Treetop Tree House
https://adventofcode.com/2022/day/8
"""

import numba as nb
import numpy as np


@nb.jit(["int64(int64[:, :], int64, int64)"], nopython=True, cache=True)
def is_visible(m: np.ndarray, i: int, j: int) -> bool:
    all_smaller = True
    for i_ in np.arange(i - 1, -1, -1):
        if m[i_, j] >= m[i, j]:
            all_smaller = False
            break

    if all_smaller:
        return True

    all_smaller = True
    for i_ in np.arange(i + 1, m.shape[0]):
        if m[i_, j] >= m[i, j]:
            all_smaller = False
            break

    if all_smaller:
        return True

    all_smaller = True
    for j_ in np.arange(j - 1, -1, -1):
        if m[i, j_] >= m[i, j]:
            all_smaller = False
            break

    if all_smaller:
        return True

    all_smaller = True
    for j_ in np.arange(j + 1, m.shape[1]):
        if m[i, j_] >= m[i, j]:
            all_smaller = False
            break

    if all_smaller:
        return True

    return False


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    21
    """
    s = s.strip("\n")
    m = np.array([[int(x) for x in line] for line in s.splitlines()])
    visible = 0
    for i in range(1, m.shape[0] - 1):
        for j in range(1, m.shape[1] - 1):
            if is_visible(m, i, j):
                visible += 1

    return visible + 2 * (m.shape[0] - 1 + m.shape[1] - 1)


@nb.jit(["int64(int64[:, :], int64, int64)"], nopython=True, cache=True)
def get_score(m: np.ndarray, i: int, j: int) -> int:
    score = 1

    for i_ in np.arange(i - 1, -1, -1):
        if m[i_, j] >= m[i, j]:
            break

    score *= i - i_

    for i_ in np.arange(i + 1, m.shape[0]):
        if m[i_, j] >= m[i, j]:
            break

    score *= i_ - i

    for j_ in np.arange(j - 1, -1, -1):
        if m[i, j_] >= m[i, j]:
            break

    score *= j - j_

    for j_ in np.arange(j + 1, m.shape[1]):
        if m[i, j_] >= m[i, j]:
            break

    score *= j_ - j

    return score


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    8
    """
    s = s.strip("\n")
    m = np.array([[int(x) for x in line] for line in s.splitlines()])
    max_score = 0
    for i in range(1, m.shape[0] - 1):
        for j in range(1, m.shape[1] - 1):
            max_score = max(max_score, get_score(m, i, j))

    return max_score


test_string = """
30373
25512
65332
33549
35390
"""
solve_a(test_string)
solve_b(test_string)

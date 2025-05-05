import numpy as np


def solve_a(s: str) -> int:
    mat = np.array([list(line) for line in s.split("\n")])
    n, m = mat.shape
    mat = np.pad(mat, pad_width=[(0, 0), (0, 3 * n)], mode="wrap")
    return sum(1 if mat[i, 3 * i] == "#" else 0 for i in range(n))


def solve_b(s: str) -> int:
    mat = np.array([list(line) for line in s.split("\n")])
    n, m = mat.shape
    mat = np.pad(mat, pad_width=[(0, 0), (0, 7 * n)], mode="wrap")
    trees_slope_11 = sum(1 if mat[i, i] == "#" else 0 for i in range(n))
    trees_slope_31 = sum(1 if mat[i, 3 * i] == "#" else 0 for i in range(n))
    trees_slope_51 = sum(1 if mat[i, 5 * i] == "#" else 0 for i in range(n))
    trees_slope_71 = sum(1 if mat[i, 7 * i] == "#" else 0 for i in range(n))
    trees_slope_12 = sum(1 if mat[2 * i, i] == "#" else 0 for i in range(n // 2))
    return trees_slope_11 * trees_slope_31 * trees_slope_51 * trees_slope_71 * trees_slope_12

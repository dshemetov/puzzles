"""Dumbo Octopus
https://adventofcode.com/2021/day/11
"""

from itertools import product

import numpy as np


def solve_a(s: str) -> int:
    _, flashes = run_octopus_steps(parse_input(s), 100)
    return flashes


def parse_input(s: str) -> np.ndarray:
    return np.array([list(line) for line in s.split("\n")], dtype=int)


def run_octopus_step(mat: np.ndarray) -> tuple[np.ndarray, int]:
    mat = mat.copy()
    mat += 1
    n, m = mat.shape
    already_flashed = set()
    ixs_to_check = set((i, j) for i, j in product(range(n), range(m)) if mat[i, j] > 9)
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1), (1, 1), (-1, -1), (-1, 1), (1, -1)]

    while len(ixs_to_check) > 0:
        i, j = ixs_to_check.pop()
        if mat[i, j] > 9 and (i, j) not in already_flashed:
            already_flashed |= {(i, j)}
            for i_, j_ in [(i + directions[0], j + directions[1]) for directions in directions]:
                mat[i_, j_] += 1
                ixs_to_check |= {(i_, j_)}
    mat[np.where(mat > 9)] = 0
    return mat, len(already_flashed)


def run_octopus_steps(mat: np.ndarray, n: int) -> tuple[np.ndarray, int]:
    flash_counter = 0
    mat_ = mat.copy()
    for _ in range(n):
        mat_, flashes = run_octopus_step(mat_)
        flash_counter += flashes
    return mat_, flash_counter


def solve_b(s: str) -> int:
    mat = parse_input(s)
    i = 1
    while True:
        mat, _ = run_octopus_step(mat)
        if (mat == 0).all():
            break
        i += 1
    return i


test_string_10 = [
    """5483143223
2745854711
5264556173
6141336146
6357385478
4167524645
2176841721
6882881134
4846848554
5283751526""",
    """0481112976
0031112009
0041112504
0081111406
0099111306
0093511233
0442361130
5532252350
0532250600
0032240000""",
    """3936556452
5686556806
4496555690
4448655580
4456865570
5680086577
7000009896
0000000344
6000000364
4600009543""",
    """0643334118
4253334611
3374333458
2225333337
2229333338
2276733333
2754574565
5544458511
9444447111
7944446119""",
    """0397666866
0749766918
0053976933
0004297822
0004229892
0053222877
0532222966
9322228966
7922286866
6789998766""",
]

test_string_5 = [
    """11111
19991
19191
19991
11111""",
    """34543
40004
50005
40004
34543""",
    """45654
51115
61116
51115
45654""",
]


def test_solve_a():
    mat0 = parse_input(test_string_5[0])
    out_mat, out_flashes = run_octopus_step(mat0)
    expected_mat = parse_input(test_string_5[1])
    np.testing.assert_allclose(out_mat, expected_mat)
    assert out_flashes == 9
    out_mat, out_flashes = run_octopus_step(out_mat)
    expected_mat = parse_input(test_string_5[2])
    np.testing.assert_allclose(out_mat, expected_mat)
    assert out_flashes == len(expected_mat[np.where(expected_mat == 0)])

    mat0 = parse_input(test_string_10[0])
    _, out_flashes = run_octopus_steps(mat0, 10)
    expected_mat = parse_input(test_string_10[1])
    assert out_flashes == 204

    mat0 = parse_input(test_string_10[0])
    out_mat, out_flashes = run_octopus_steps(mat0, 20)
    expected_mat = parse_input(test_string_10[2])
    np.testing.assert_allclose(out_mat, expected_mat)

    mat0 = parse_input(test_string_10[0])
    out_mat, out_flashes = run_octopus_steps(mat0, 30)
    expected_mat = parse_input(test_string_10[3])
    np.testing.assert_allclose(out_mat, expected_mat)

    mat0 = parse_input(test_string_10[0])
    out_mat, out_flashes = run_octopus_steps(mat0, 100)
    expected_mat = parse_input(test_string_10[4])
    np.testing.assert_allclose(out_mat, expected_mat)

    assert solve_a(test_string_10[0]) == 1656


def test_solve_b():
    assert solve_b(test_string_10[0]) == 195

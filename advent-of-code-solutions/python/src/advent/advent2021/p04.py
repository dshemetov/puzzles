"""Giant Squid
https://adventofcode.com/2021/day/4
"""

import numpy as np


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    4512
    """
    batches = s.split("\n\n")
    numbers = [int(num) for num in batches[0].split(",")]
    boards = np.stack([board_from_str(board_str) for board_str in batches[1:]])
    n_boards, n, m = boards.shape
    board_masks = np.zeros((n_boards, n, m))

    have_winner = False
    for num in numbers:
        for i in range(n_boards):
            board_masks[i][np.where(boards[i] == num)] = 1
            if did_board_win(board_masks[i]):
                have_winner = True
                break
        if have_winner:
            break

    return int(get_board_score(boards[i], board_masks[i], num))


def board_from_str(s: str) -> np.ndarray:
    return np.array([line.split() for line in s.split("\n")], dtype=int)


def did_board_win(board_mask: np.ndarray) -> bool:
    return board_mask.all(axis=0).any() or board_mask.all(axis=1).any()


def get_board_score(board: np.ndarray, board_mask: np.ndarray, last_num: int) -> int:
    return board[~board_mask.astype(bool)].sum() * last_num


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    1924
    """
    batches = s.split("\n\n")
    numbers = [int(num) for num in batches[0].split(",")]
    boards = np.stack([board_from_str(board_str) for board_str in batches[1:]])
    n_boards, n, m = boards.shape
    board_masks = np.zeros((n_boards, n, m))

    winner_boards = set()
    for num in numbers:
        for i in range(n_boards):
            board_masks[i][np.where(boards[i] == num)] = 1
            if did_board_win(board_masks[i]):
                winner_boards |= set([i])
                if len(winner_boards) == n_boards:
                    break
        if len(winner_boards) == n_boards:
            break

    return int(get_board_score(boards[i], board_masks[i], num))


test_string = """7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7"""

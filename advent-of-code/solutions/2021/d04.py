# /// script
# requires-python = ">=3.14"
# dependencies = ["numpy"]
# ///
"""Giant Squid
https://adventofcode.com/2021/day/4
"""

import sys
import time

import numpy as np


def part_a(s: str) -> int:
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


def part_b(s: str) -> int:
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


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

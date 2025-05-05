"""3. Gear Ratios https://adventofcode.com/2023/day/3

Minor flex: ran correctly first try.
"""

from itertools import product
from math import prod


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    4361
    """
    board = [list(line) for line in s.strip("\n").splitlines()]

    total = 0
    seen = set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != "." and not board[i][j].isdigit():
                for di, dj in product(range(-1, 2), repeat=2):
                    i_, j_ = i + di, j + dj
                    if (
                        0 <= i_ < len(board)
                        and 0 <= j_ < len(board[0])
                        and board[i_][j_].isdigit()
                        and (i_, j_) not in seen
                    ):
                        num_list = [board[i_][j_]]
                        seen.add((i_, j_))
                        for j__ in range(j_ + 1, len(board[0])):
                            if board[i_][j__].isdigit():
                                num_list.append(board[i_][j__])
                                seen.add((i_, j__))
                            else:
                                break
                        for j__ in range(j_ - 1, -1, -1):
                            if board[i_][j__].isdigit():
                                num_list.insert(0, board[i_][j__])
                                seen.add((i_, j__))
                            else:
                                break
                        total += int("".join(num_list))

    return total


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    467835
    """
    board = [list(line) for line in s.strip("\n").splitlines()]

    total = 0
    seen = set()
    for i in range(len(board)):
        for j in range(len(board[0])):
            if board[i][j] != "." and not board[i][j].isdigit():
                gear_nums = []
                for di, dj in product(range(-1, 2), repeat=2):
                    i_, j_ = i + di, j + dj
                    if (
                        0 <= i_ < len(board)
                        and 0 <= j_ < len(board[0])
                        and board[i_][j_].isdigit()
                        and (i_, j_) not in seen
                    ):
                        num_list = [board[i_][j_]]
                        seen.add((i_, j_))
                        for j__ in range(j_ + 1, len(board[0])):
                            if board[i_][j__].isdigit():
                                num_list.append(board[i_][j__])
                                seen.add((i_, j__))
                            else:
                                break
                        for j__ in range(j_ - 1, -1, -1):
                            if board[i_][j__].isdigit():
                                num_list.insert(0, board[i_][j__])
                                seen.add((i_, j__))
                            else:
                                break
                        gear_nums.append(int("".join(num_list)))

                if len(gear_nums) == 2:
                    total += prod(gear_nums)

    return total


test_string = """
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
"""

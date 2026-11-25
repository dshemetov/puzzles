from dataclasses import dataclass
from itertools import product


def p37(board: list[list[str]]) -> None:
    """37. Sudoku Solver https://leetcode.com/problems/sudoku-solver/

    Modifies board in-place.

    Example:
    >>> board = [
    ...     ["5", "3", ".", ".", "7", ".", ".", ".", "."],
    ...     ["6", ".", ".", "1", "9", "5", ".", ".", "."],
    ...     [".", "9", "8", ".", ".", ".", ".", "6", "."],
    ...     ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
    ...     ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
    ...     ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
    ...     [".", "6", ".", ".", ".", ".", "2", "8", "."],
    ...     [".", ".", ".", "4", "1", "9", ".", ".", "5"],
    ...     [".", ".", ".", ".", "8", ".", ".", "7", "9"],
    ... ]
    >>> p37(board)
    >>> board
    [['5', '3', '4', '6', '7', '8', '9', '1', '2'], ['6', '7', '2', '1', '9', '5', '3', '4', '8'], ['1', '9', '8', '3', '4', '2', '5', '6', '7'], ['8', '5', '9', '7', '6', '1', '4', '2', '3'], ['4', '2', '6', '8', '5', '3', '7', '9', '1'], ['7', '1', '3', '9', '2', '4', '8', '5', '6'], ['9', '6', '1', '5', '3', '7', '2', '8', '4'], ['2', '8', '7', '4', '1', '9', '6', '3', '5'], ['3', '4', '5', '2', '8', '6', '1', '7', '9']]
    """
    from copy import deepcopy
    from dataclasses import field

    all_digits = {str(x) for x in range(1, 10)}

    @dataclass
    class Cell:
        i: int
        j: int
        val: str = "."
        options: set = field(default_factory=set)

    @dataclass
    class Board:
        cells: list[Cell]

    # TODO: Need to make that allowed choices for filled-in cells is empty.

    _board = Board([Cell(i, j, ".", deepcopy(all_digits)) for i in range(9) for j in range(9)])
    for i, j in product(range(9), range(9)):
        cell = _board.cells[i * 9 + j]
        if board[i][j] == ".":
            cell.options -= {board[i][k] for k in range(9)}
            cell.options -= {board[k][j] for k in range(9)}
            cell.options -= {board[3 * (i // 3) + di][3 * (j // 3) + dj] for di in range(3) for dj in range(3)}
        else:
            cell.val = board[i][j]
            cell.options = set()

    def push_allowed_map(i: int, j: int, val: str) -> None:
        ix = i * 9 + j
        _board.cells[ix] = Cell(i, j, val, set())
        for k in range(9):
            if i * 9 + k != ix:
                _board.cells[i * 9 + k].options.discard(val)
            if k * 9 + j != ix:
                _board.cells[k * 9 + j].options.discard(val)
            if (3 * (i // 3) + k // 3) * 9 + (3 * (j // 3) + k % 3) != ix:
                _board.cells[(3 * (i // 3) + k // 3) * 9 + (3 * (j // 3) + k % 3)].options.discard(val)

    def pop_allowed_map(i: int, j: int, val: str) -> None:
        ix = i * 9 + j
        _board.cells[ix] = Cell(i, j, ".", deepcopy(all_digits))
        _board.cells[ix].options -= {
            _board.cells[i * 9 + k].val for k in range(9) if _board.cells[i * 9 + k].val != "."
        }
        _board.cells[ix].options -= {
            _board.cells[k * 9 + j].val for k in range(9) if _board.cells[k * 9 + j].val != "."
        }
        _board.cells[ix].options -= {
            _board.cells[(3 * (i // 3) + di) * 9 + (3 * (j // 3) + dj)].val
            for di in range(3)
            for dj in range(3)
            if _board.cells[(3 * (i // 3) + di) * 9 + (3 * (j // 3) + dj)].val != "."
        }
        for k in range(9):
            if i * 9 + k != ix:
                _board.cells[i * 9 + k].options.add(val)
            if k * 9 + j != ix:
                _board.cells[k * 9 + j].options.add(val)
            if (3 * (i // 3) + k // 3) * 9 + (3 * (j // 3) + k % 3) != ix:
                _board.cells[(3 * (i // 3) + k // 3) * 9 + (3 * (j // 3) + k % 3)].options.add(val)

    def print_board() -> None:
        for i in range(9):
            print(" ".join(c.val for c in _board.cells[i * 9 : (i + 1) * 9]))
        print()

    q = 0

    def recurse(choices: list[Cell]) -> tuple[bool, list]:
        nonlocal q
        q += 1
        print("Recursion depth:", q)
        print("Last choice:", choices[-1] if choices else None)
        print_board()
        if q == 10:
            return False, choices

        if any(
            _board.cells[i * 9 + j].val == "." and not _board.cells[i * 9 + j].options
            for i, j in product(range(9), range(9))
        ):
            print("No options for some cell, backing out.")
            return False, choices

        open_cells = sorted([c for c in _board.cells if c.val == "."], key=lambda x: len(x.options))

        if not open_cells:
            print("No open cells, found solution.")
            return True, choices

        for cell in open_cells:
            results = []
            for c in cell.options:
                push_allowed_map(cell.i, cell.j, c)
                choices = choices + [Cell(cell.i, cell.j, c)]
                results.append(recurse(choices)[0])
                if results[-1]:
                    return (True, choices)
                pop_allowed_map(cell.i, cell.j, c)
                choices.pop()
            if not any(results):
                print("None of the options for cell", cell, "worked:", results)
                return (False, choices)

        return (False, choices)

    # print("hello")
    # print(_board)
    possible, choices = recurse([])
    if possible:
        for cell in choices:
            board[cell.i][cell.j] = cell.val
        return

    raise ValueError("No solution exists")

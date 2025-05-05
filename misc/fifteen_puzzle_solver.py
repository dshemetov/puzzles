# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "numpy",
# ]
# ///
from heapq import heappop, heappush
from typing import Callable
from unittest import skip

from numpy import abs, allclose, arange, argwhere, array, int64, ndarray, where
from numpy.random import choice

N = 4
END_STATE = arange(1, N**2 + 1).reshape(N, N)
EMPTY_SPACE = N**2


def get_move_location(move: int, state: ndarray) -> ndarray:
    return argwhere(state == move)


def get_number_at_location(loc: ndarray, state: ndarray) -> int:
    return state[tuple(loc)]


def check_valid_move(move: int, state: ndarray) -> bool:
    loc1, loc2 = get_move_location(move, state), get_move_location(EMPTY_SPACE, state)
    return True if abs(loc1 - loc2).sum() == 1 else False


def get_valid_moves(state: ndarray) -> list[int]:
    n, _ = state.shape
    move_location = get_move_location(EMPTY_SPACE, state)
    directions = array([[1, 0], [0, 1], [-1, 0], [0, -1]])
    possible_moves = move_location + directions
    valid_locations = [move for move in possible_moves if all((0 <= move) & (move < n))]
    moves = sorted([get_number_at_location(loc, state) for loc in valid_locations])
    return moves


def make_moves(moves: int | list[int], state: ndarray) -> ndarray:
    """Attempt to make moves, if valid.

    Moves are represented by numbers 1-15, corresponding to which number will be
    pushed in the empty space. A list of moves is performed sequentially with
    index 0 going first.
    """
    if isinstance(moves, (int, int64)):
        move = moves
        if not check_valid_move(move, state):
            raise ValueError("Invalid move.")

        new_state = state.copy()
        loc1, loc2 = where(new_state == move), where(new_state == EMPTY_SPACE)
        new_state[loc1], new_state[loc2] = EMPTY_SPACE, move

    if isinstance(moves, list):
        current_state = state
        for move in moves:
            current_state = make_moves(move, current_state)
        new_state = current_state

    return new_state


def make_random_moves(start_state: ndarray, n: int) -> tuple[ndarray, list[int]]:
    current_state = start_state
    moves = []
    for _ in range(n):
        move = choice(get_valid_moves(current_state))
        moves.append(move)
        current_state = make_moves(move, current_state)
    return current_state, moves


def manhattan_heuristic(state1: ndarray, state2: ndarray) -> int:
    """Return the Manhattan heuristic distance between two states.

    The Manhattan heuristic is defined as the sum of the Manhattan distances between the
    coordinates of each number.
    """
    s = 0
    for number in range(1, state1.shape[0] ** 2 + 1):
        loc1, loc2 = (
            get_move_location(number, state1),
            get_move_location(number, state2),
        )
        s += abs(loc1 - loc2).sum()
    return s


def trivial_heuristic(*args) -> int:
    return 0


def a_star(
    start_state: ndarray,
    end_state: ndarray = END_STATE,
    heuristic_weight: float = 1.0,
    heuristic_distance: Callable = manhattan_heuristic,
) -> list[int]:
    """Run the A* algorithm to find the shortest path between two states.

    The priority queue is a list of tuples (priority, path_sequence), where
    path_sequence is the sequence of moves taken so far and priority is given by
    (length of path so far) + heuristic_weight * heuristic_distance between the
    resulting state and the desired end state. Under the hood, the priority
    queue is implemented through a binary heap, see
    https://docs.python.org/3/library/heapq.html for details. We rederive the
    resulting state from the path sequence instead of storing it because the
    priority queue expects tuples where each dimension has an ordering defined.
    """
    priority_queue = []
    current_state, current_moves = start_state, []
    best_dict = dict()

    while not allclose(current_state, end_state):
        valid_moves = get_valid_moves(current_state)
        if current_moves:
            valid_moves = [move for move in valid_moves if move != current_moves[-1]]
        for move in valid_moves:
            distance = (
                1
                + len(current_moves)
                + heuristic_weight
                * heuristic_distance(make_moves(move, current_state), end_state)
            )
            if distance < best_dict.get(tuple(current_state.flatten()), float("inf")):
                best_dict[tuple(current_state.flatten())] = distance
                heappush(priority_queue, (distance, current_moves + [move]))
        d, current_moves = heappop(priority_queue)
        current_state = make_moves(current_moves, start_state)
        print(d)
        print(current_state)

    return current_moves


class TestSolver:
    def test_get_move_location(self):
        state = array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 16], [13, 14, 15, 12]])
        assert (get_move_location(11, state) == array([2, 2])).all()

    def test_get_number_at_location(self):
        state = array([[1, 2, 3, 4], [5, 6, 7, 8], [9, 10, 11, 16], [13, 14, 15, 12]])
        assert get_number_at_location(array([2, 2]), state) == 11

    def test_check_valid_move(self):
        assert check_valid_move(12, END_STATE)
        assert not check_valid_move(11, END_STATE)

    def test_get_valid_moves(self):
        assert allclose(get_valid_moves(END_STATE), [12, 15])

    def test_make_moves(self):
        # fmt: off
        expected_state = array([
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 11, 16],
            [13, 14, 15, 12]
        ])
        assert allclose(make_moves(12, END_STATE), expected_state)
        start_state = array([
            [1, 2, 3, 4],
            [5, 6, 7, 8],
            [9, 10, 16, 11],
            [13, 14, 15, 12]
        ])
        # fmt: on
        assert allclose(make_moves([11, 12], start_state), END_STATE)
        assert allclose(get_valid_moves(make_moves(12, END_STATE)), [8, 11, 12])

    def test_manhattain_distance_number(self):
        assert manhattan_heuristic(END_STATE, END_STATE) == 0
        assert manhattan_heuristic(make_moves(12, END_STATE), END_STATE) == 2

    def test_a_star(self):
        # Short deterministic test
        moves = [12, 11, 7]
        start_state = make_moves(moves, END_STATE.copy())
        solution = a_star(start_state, END_STATE)
        assert allclose(solution, list(reversed(moves)))

        # Random test
        start_state, moves = make_random_moves(END_STATE.copy(), 30)
        solution = a_star(start_state, END_STATE)
        assert allclose(make_moves(solution, start_state), END_STATE)

    @skip("This test is too slow.")
    def test_hard_case(self):
        start_state = array(
            [[1, 8, 16, 7], [2, 3, 4, 13], [14, 9, 15, 6], [11, 10, 12, 5]]
        )
        solution = a_star(start_state, END_STATE)
        assert allclose(make_moves(solution, start_state), END_STATE)

    @skip("This test is too slow.")
    def test_extremely_hard_case(self):
        # The hardest test, requires 80 moves
        # https://puzzling.stackexchange.com/questions/24265/what-is-the-superflip-on-15-puzzle
        start_state = array(
            [[15, 14, 8, 12], [10, 11, 9, 13], [2, 6, 5, 1], [3, 4, 7, EMPTY_SPACE]]
        )
        solution = a_star(start_state, END_STATE)
        assert len(solution) == 80


start_state = array([[1, 8, 16, 7], [2, 3, 4, 13], [14, 9, 15, 6], [11, 10, 12, 5]])
solution = a_star(start_state, END_STATE)
print(solution)

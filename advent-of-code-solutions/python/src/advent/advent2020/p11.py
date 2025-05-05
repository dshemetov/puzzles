from copy import deepcopy
from itertools import product
from typing import Iterable


def solve_a(s: str) -> int:
    state = string_to_array(s)
    return count_occupied_seats(update_state_until_fixed(state, "nearby"))


def string_to_array(s: str) -> list[list[str]]:
    return [list(x) for x in s.strip("\n").split("\n")]


def count_occupied_seats(state: list[list[str]]) -> int:
    return sum(1 for row in state for x in row if x == "#")


def update_state_until_fixed(state: list[list[str]], method: str) -> list[list[str]]:
    current_state = deepcopy(state)
    next_state = deepcopy(state)
    no_changes = False
    while no_changes is False:
        no_changes = True
        newly_occupied_seats, newly_vacant_seats = find_seats_to_update(current_state, method)
        for i, j in newly_occupied_seats:
            next_state[i][j] = "#"
            no_changes = False
        for i, j in newly_vacant_seats:
            next_state[i][j] = "L"
            no_changes = False
        current_state = deepcopy(next_state)
    return next_state


def find_seats_to_update(state: list[list[str]], method: str) -> list[list[str]]:
    if method == "nearby":
        newly_occupied_seats = ((i, j) for i, j in get_empty_seats(state) if check_nearby_seats_empty(i, j, state))
        newly_vacant_seats = ((i, j) for i, j in get_occupied_seats(state) if check_nearby_seats_crowded(i, j, state))
    if method == "visible":
        newly_occupied_seats = ((i, j) for i, j in get_empty_seats(state) if check_visible_seats_empty(i, j, state))
        newly_vacant_seats = ((i, j) for i, j in get_occupied_seats(state) if check_visible_seats_crowded(i, j, state))
    return newly_occupied_seats, newly_vacant_seats


def get_empty_seats(state: list[list[str]]) -> Iterable[tuple[int, int]]:
    n, m = len(state), len(state[0])
    for i, j in product(range(n), range(m)):
        if state[i][j] == "L":
            yield i, j


def get_occupied_seats(state: list[list[str]]) -> Iterable[tuple[int, int]]:
    n, m = len(state), len(state[0])
    for i, j in product(range(n), range(m)):
        if state[i][j] == "#":
            yield i, j


def check_nearby_seats_empty(i: int, j: int, state: list[list[str]]) -> bool:
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    n, m = len(state), len(state[0])
    for i_, j_ in [(i + di, j + dj) for di, dj in directions if 0 <= i + di < n and 0 <= j + dj < m]:
        if state[i_][j_] == "#":
            return False
    return True


def check_nearby_seats_crowded(i: int, j: int, state: list[list[str]]) -> bool:
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (-1, -1), (1, -1), (-1, 1)]
    n, m = len(state), len(state[0])
    visible_seats = 0
    for i_, j_ in [(i + di, j + dj) for di, dj in directions if 0 <= i + di < n and 0 <= j + dj < m]:
        if state[i_][j_] == "#":
            visible_seats += 1
            if visible_seats >= 4:
                return True
    return False


def check_visible_seats_empty(i: int, j: int, state: list[list[str]]) -> bool:
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    for di, dj in directions:
        if "#" == get_first_visible_object(i, j, di, dj, state):
            return False
    return True


def check_visible_seats_crowded(i: int, j: int, state: list[list[str]]) -> bool:
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    visible_seats = 0
    for di, dj in directions:
        if "#" == get_first_visible_object(i, j, di, dj, state):
            visible_seats += 1
            if visible_seats >= 5:
                return True
    return False


def get_first_visible_object(i: int, j: int, di: int, dj: int, state: list[list[str]]) -> str:
    n, m = len(state), len(state[0])
    i_, j_ = i + di, j + dj
    while (0 <= i_ < n) and (0 <= j_ < m):
        v = state[i_][j_]
        if v == "#":
            return "#"
        if v == "L":
            return "L"
        i_, j_ = i_ + di, j_ + dj
    return "."


def solve_b(s: str) -> int:
    state = string_to_array(s)
    return count_occupied_seats(update_state_until_fixed(state, "visible"))


test_string = "L.LL.LL.LL\nLLLLLLL.LL\nL.L.L..L..\nLLLL.LL.LL\nL.LL.LL.LL\nL.LLLLL.LL\n..L.L.....\nLLLLLLLLLL\nL.LLLLLL.L\nL.LLLLL.LL\n"
next_states_a = [
    "#.##.##.##\n#######.##\n#.#.#..#..\n####.##.##\n#.##.##.##\n#.#####.##\n..#.#.....\n##########\n#.######.#\n#.#####.##\n",
    "#.LL.L#.##\n#LLLLLL.L#\nL.L.L..L..\n#LLL.LL.L#\n#.LL.LL.LL\n#.LLLL#.##\n..L.L.....\n#LLLLLLLL#\n#.LLLLLL.L\n#.#LLLL.##\n",
    "#.##.L#.##\n#L###LL.L#\nL.#.#..#..\n#L##.##.L#\n#.##.LL.LL\n#.###L#.##\n..#.#.....\n#L######L#\n#.LL###L.L\n#.#L###.##\n",
    "#.#L.L#.##\n#LLL#LL.L#\nL.L.L..#..\n#LLL.##.L#\n#.LL.LL.LL\n#.LL#L#.##\n..L.L.....\n#L#LLLL#L#\n#.LLLLLL.L\n#.#L#L#.##\n",
    "#.#L.L#.##\n#LLL#LL.L#\nL.#.L..#..\n#L##.##.L#\n#.#L.LL.LL\n#.#L#L#.##\n..L.L.....\n#L#L##L#L#\n#.LLLLLL.L\n#.#L#L#.##",
]
next_states_b = [
    "#.##.##.##\n#######.##\n#.#.#..#..\n####.##.##\n#.##.##.##\n#.#####.##\n..#.#.....\n##########\n#.######.#\n#.#####.##\n",
    "#.LL.LL.L#\n#LLLLLL.LL\nL.L.L..L..\nLLLL.LL.LL\nL.LL.LL.LL\nL.LLLLL.LL\n..L.L.....\nLLLLLLLLL#\n#.LLLLLL.L\n#.LLLLL.L#",
    "#.L#.##.L#\n#L#####.LL\nL.#.#..#..\n##L#.##.##\n#.##.#L.##\n#.#####.#L\n..#.#.....\nLLL####LL#\n#.L#####.L\n#.L####.L#",
    "#.L#.L#.L#\n#LLLLLL.LL\nL.L.L..#..\n##LL.LL.L#\nL.LL.LL.L#\n#.LLLLL.LL\n..L.L.....\nLLLLLLLLL#\n#.LLLLL#.L\n#.L#LL#.L#",
    "#.L#.L#.L#\n#LLLLLL.LL\nL.L.L..#..\n##L#.#L.L#\nL.L#.#L.L#\n#.L####.LL\n..#.#.....\nLLL###LLL#\n#.LLLLL#.L\n#.L#LL#.L#",
    "#.L#.L#.L#\n#LLLLLL.LL\nL.L.L..#..\n##L#.#L.L#\nL.L#.LL.L#\n#.LLLL#.LL\n..#.L.....\nLLL###LLL#\n#.LLLLL#.L\n#.L#LL#.L#",
]


def test_update_state_until_fixed():
    # Part a
    current_state = string_to_array(test_string)
    current_state = update_state_until_fixed(current_state, "nearby")
    assert current_state == string_to_array(next_states_a[4])

    # Part b
    current_state = string_to_array(test_string)
    current_state = update_state_until_fixed(current_state, "visible")
    assert current_state == string_to_array(next_states_b[5])


def test_count_occupied_seats():
    # Part a
    current_state = string_to_array(test_string)
    current_state = update_state_until_fixed(current_state, "nearby")
    assert count_occupied_seats(current_state) == 37

    # Part b
    current_state = string_to_array(test_string)
    current_state = update_state_until_fixed(current_state, "visible")
    assert count_occupied_seats(current_state) == 26

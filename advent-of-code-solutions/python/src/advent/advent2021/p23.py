"""23. Amphipod https://adventofcode.com/2021/day/23

Notes:

- This problem is not so hard algorithmically - it's just A star search.
  However, the main challenge is to reduce the branching factor as much as
  possible. The first part was simple enough to solve manually and I then
  tackled it with a very unoptimized movement strategy. The second part took
  more thought. Looking at other solutions, I thought that maybe my problem
  representation was too bulky (others on Reddit, such as Gravitar64, used a
  simple string representation, see below), but that was not the case (my final
  solution is within a factor of 2 of Gravitar64's). The main gain came from not
  moving amphipods into rooms if there are still amphipods that needed to move
  out of that room.

    https://github.com/Gravitar64/Advent-of-Code-2021/blob/main/Tag_23.py

- Interestingly, the A star heuristic only helps for part 1. For part 2, the
  solution slows down by 50% if the heuristic is used. I suppose this means the
  actual solution requires a lot of diversions from the heuristic.
- This is my solution for part A, solved manually:

cost = 0
#############
#...........# ###C#C#A#B###
  #D#D#B#A#
  #########

cost += 7A + 2B + 9A + 5B + 6C + 5C
#############
#AA.B.....B.# ###.#.#C#.###
  #D#D#C#.#
  #########

cost += 8D + 3B + 6B + 9D + 3A + 3A
#############
#...........# ###A#B#C#D###
  #A#B#C#D#
  #########

"""

from collections import defaultdict, namedtuple
from dataclasses import dataclass, field
from functools import lru_cache
from heapq import heappop, heappush
from typing import Callable

from advent.tools import get_puzzle_input

EXAMPLE2 = """
#############
#...........#
###B#C#B#D###
  #A#D#C#A#
  #########
"""
EXAMPLE4 = """
#############
#...........#
###B#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########
"""
GOAL2 = """
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #########
"""
GOAL4 = """
#############
#...........#
###A#B#C#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#D#
  #########
"""
EMPTY_BOARD2 = """
#############
#...........#
###.#.#.#.###
  #.#.#.#.#
  #########
"""
EMPTY_BOARD4 = """
#############
#...........#
###.#.#.#.###
  #.#.#.#.#
  #.#.#.#.#
  #.#.#.#.#
  #########
"""
Amphipod = namedtuple("Amphipod", ["x", "y", "type"])


@dataclass
class BoardState:
    """Full state of the board.

    The cost is the number of steps taken so far and moves records the moves
    taken so far. The coordinates are indexed as follows (where A = 10):

      X   0123456789A
    Y    #############
    0    #...........#
    1    ###.#.#.#.###
    2      #.#.#.#.#
    3      #.#.#.#.#
    4      #.#.#.#.#
           #########

    """

    amphipods: list[Amphipod]
    cost: int = 0
    moves: list[tuple[int, tuple[int, int]]] = field(default_factory=list)

    def __lt__(self, other: "BoardState"):
        return self.cost < other.cost or self.amphipods < other.amphipods

    def __repr__(self):
        room_size = 2 if len(self.amphipods) == 8 else 4
        if room_size == 2:
            rooms = [list(line) for line in EMPTY_BOARD2.strip().splitlines()]
        else:
            rooms = [list(line) for line in EMPTY_BOARD4.strip().splitlines()]

        for x, y, t in self.amphipods:
            rooms[y + 1][x + 1] = t

        return "\n".join("".join(line) for line in rooms)

    @classmethod
    def from_string(cls, s: str) -> "BoardState":
        lines = s.strip().splitlines()
        return cls(
            [
                Amphipod(i, j, type)
                for j, line in enumerate(lines[1 : len(lines) - 1])
                for i, type in enumerate(line[1:-1])
                if type in {"A", "B", "C", "D"}
            ]
        )


def get_valid_moves(b: BoardState) -> list[tuple[int, tuple[int, int]]]:
    room_size = 2 if len(b.amphipods) == 8 else 4
    valid_moves = []

    # Partition the pods.
    hallway_pods = []
    pods_by_room = {"A": [], "B": [], "C": [], "D": []}
    for i, pod in enumerate(b.amphipods):
        if pod.y == 0:
            hallway_pods += [(i, pod)]
        else:
            pods_by_room[chr(pod.x // 2 - 1 + ord("A"))].append((i, pod))

    # First find pods that could move to rooms.
    maybe_moves = []
    for i, pod in hallway_pods:
        target_room = 2 * (ord(pod.type) - ord("A") + 1)
        if not pods_by_room[pod.type]:
            maybe_moves += [(i, (target_room, room_size))]
        elif all(pod.type == pod_.type for _, pod_ in pods_by_room[pod.type]):
            available_room = min(pod_.y for _, pod_ in pods_by_room[pod.type]) - 1
            maybe_moves += [(i, (target_room, available_room))]

    # Next find top of stack pods that could move to hallway.
    for type, room_pods in pods_by_room.items():
        target_room = 2 * (ord(type) - ord("A") + 1)
        if not room_pods:
            continue
        if not all(pod.type == type for _, pod in room_pods):
            i, pod = sorted(room_pods, key=lambda x: x[1].y)[0]
            maybe_moves += [(i, (i_, 0)) for i_ in [0, 1, 3, 5, 7, 9, 10]]

    valid_moves += [(i, move) for i, move in maybe_moves if check_valid_move(b, b.amphipods[i][0:2], move)]
    return valid_moves


def check_valid_move(
    b: BoardState,
    s: tuple[int, int],
    t: tuple[int, int],
) -> bool:
    if s == t:
        return False
    if s[1] == t[1] == 0:
        return False

    path = get_path(s, t)
    for pod in b.amphipods:
        if (pod.x, pod.y) in path:
            return False

    return True


def make_move(b: BoardState, i: int, t: tuple[int, int]) -> BoardState:
    s = b.amphipods[i][0:2]
    type = b.amphipods[i].type
    b_ = BoardState(b.amphipods.copy(), b.cost, b.moves.copy())
    b_.amphipods[i] = Amphipod(t[0], t[1], type)
    b_.cost += get_move_cost(s, t) * 10 ** (ord(type) - ord("A"))
    b_.moves.append((s, t))
    return b_


@lru_cache(maxsize=None)
def get_move_cost(s: tuple[int, int], t: tuple[int, int]) -> int:
    """
    Examples:
    >>> [get_move_cost((2, 1), (i, 0)) for i in range(11)] == [3, 2, 1, 2, 3, 4, 5, 6, 7, 8, 9]
    True
    >>> [get_move_cost((2, 2), (i, 0)) for i in range(11)] == [4, 3, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    True
    >>> [get_move_cost((2, 1), (i, 1)) for i in range(2, 9, 2)] == [0, 4, 6, 8]
    True
    >>> [get_move_cost((2, 2), (i, 2)) for i in range(2, 9, 2)] == [0, 6, 8, 10]
    True
    >>> get_move_cost((2, 4), (1, 0))
    5
    """
    if s[0] == t[0]:
        return abs(s[1] - t[1])
    else:
        return abs(s[0] - t[0]) + s[1] + t[1]


@lru_cache(maxsize=None)
def get_path(s: tuple[int, int], t: tuple[int, int], include_from: bool = False) -> list[tuple[int, int]]:
    if s == t:
        return []

    if s[0] == t[0]:
        if s[1] < t[1]:
            path = [(s[0], j) for j in range(s[1], t[1] + 1)]
        else:
            path = [(s[0], j) for j in range(s[1], t[1] - 1, -1)]
    else:
        path = []
        if s[1] > 0:
            path += [(s[0], j) for j in range(s[1], -1, -1)]

        if s[0] > t[0]:
            path += [(i, 0) for i in range(s[0], t[0] - 1, -1)]
        else:
            path += [(i, 0) for i in range(s[0], t[0] + 1)]

        if t[1] > 0:
            path += [(t[0], j) for j in range(0, t[1] + 1)]

    return path if include_from else path[1:]


def draw_path(b: BoardState, path: list[tuple[int, int]]) -> str:
    room_size = 2 if len(b.amphipods) == 8 else 4
    if room_size == 2:
        rooms = [list(line) for line in EMPTY_BOARD2.strip().splitlines()]
    else:
        rooms = [list(line) for line in EMPTY_BOARD4.strip().splitlines()]

    for x, y in path:
        rooms[y + 1][x + 1] = "*" if (x, y) != path[-1] else "!"

    path_str = "\n".join("".join(line) for line in rooms)
    return merge_drawings(str(b), path_str)


def merge_drawings(s1: str, s2: str) -> str:
    lines1 = s1.strip().splitlines()
    lines2 = s2.strip().splitlines()
    lines = [[c1 if c2 == "." else c2 for c1, c2 in zip(l1, l2)] for l1, l2 in zip(lines1, lines2)]
    return "\n".join("".join(line) for line in lines)


def get_heuristic_cost(b: BoardState) -> int:
    """
    The heuristic is just the Manhattan distance for each amphipod to its
    destination room (times amphipod step cost). The complication is that we
    don't want to accidentally reorder amphipods that are in the same room, so
    we make sure they keep their relative order.
    """
    room_size = 2 if len(b.amphipods) == 8 else 4
    heuristic_costs = defaultdict(list)
    for pod in b.amphipods:
        target_room = 2 * (ord(pod.type) - ord("A") + 1)
        rooms = [(target_room, j) for j in range(1, room_size + 1)]
        heuristic_costs[pod.type].append(tuple(get_move_cost(pod[0:2], room) for room in rooms))
    heuristic_cost = 0
    for k in heuristic_costs:
        available_pods = set(range(room_size))
        pod_cost = 0
        for j in range(room_size - 1, -1, -1):
            cost, pod = min((heuristic_costs[k][i][j], i) for i in available_pods)
            pod_cost += cost
            available_pods.remove(pod)
        heuristic_cost += pod_cost * 10 ** (ord(k) - ord("A"))
    return heuristic_cost


def a_star_search(
    start: BoardState,
    goal: str,
    heuristic: Callable = lambda x: 0,
    progress: bool = False,
) -> BoardState | None:
    cost = start.cost + heuristic(start)
    prio_queue = [(cost, start)]
    memo = {str(start): cost}
    j = 0
    while prio_queue:
        j += 1
        _, board = heappop(prio_queue)
        if progress and j % 2000 == 0:
            print(board)
            print(j)
        if str(board) == goal:
            return board
        for i, t in get_valid_moves(board):
            board_ = make_move(board, i, t)
            cost_ = board_.cost + heuristic(board_)
            if str(board_) in memo and memo[str(board_)] <= cost_:
                continue
            heappush(prio_queue, (cost_, board_))
            memo[str(board_)] = cost_

    return None


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(EXAMPLE1)
    12521
    """
    start_board = BoardState.from_string(s)
    ans_board = a_star_search(start_board, GOAL2.strip(), get_heuristic_cost)

    if s == get_puzzle_input(2021, 23):
        # Solved manually.
        a, b, c, d = 1, 10, 100, 1000
        ans = 7 * a + 2 * b + 9 * a + 5 * b + 6 * c + 5 * c + 8 * d + 3 * b + 6 * b + 9 * d + 3 * a + 3 * a
        assert ans == ans_board.cost

    if ans_board:
        return ans_board.cost


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(EXAMPLE1)
    44169
    """
    lines = s.strip().splitlines()
    lines.insert(3, "  #D#B#A#C#")
    lines.insert(3, "  #D#C#B#A#")
    s = "\n".join(lines)

    start_board = BoardState.from_string(s)
    ans_board = a_star_search(start_board, GOAL4.strip())

    if ans_board:
        return ans_board.cost


board = BoardState.from_string(EXAMPLE4)
board = make_move(board, 0, (10, 0))
assert (
    str(board)
    == """
#############
#..........B#
###.#C#B#D###
  #D#C#B#A#
  #D#B#A#C#
  #A#D#C#A#
  #########
""".strip()
)
board = BoardState.from_string(
    """
#############
#...........#
###A#B#D#D###
  #A#B#C#D#
  #A#B#C#D#
  #A#B#C#C#
  #########
"""
)
assert get_heuristic_cost(board) == 7700

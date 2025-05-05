"""Hill Climbing Algorithm
https://adventofcode.com/2022/day/12

Lessons learned:

- Cython and numba don't help - the bottleneck is the heapq. I don't have access
  to a resizable array in Cython/numba.
- The A* is slower than BFS in this case, because of the cost of the priority
  queue and the fact that the heuristic is weak (the true solution follows a
  spiraling path).
- Putting all the starting nodes in the priority queue at the beginning was
  another clever optimization.
"""

from heapq import heappop, heappush

import numpy as np


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    31
    """
    s = s.strip("\n")
    m = np.array([list(e) for e in s.splitlines()], dtype=str)
    start_ix = np.where(m == "S")
    end_ix = np.where(m == "E")
    m[start_ix] = "a"
    m[end_ix] = "z"
    priority_queue = [(start_ix[0][0], start_ix[1][0])]
    return get_minimum_cost(m, priority_queue, (end_ix[0][0], end_ix[1][0]))


def get_minimum_cost(mat: np.ndarray, starting_nodes: list[tuple[int, int]], end_ix: tuple[int, int]) -> int:
    """This is A* without a heuristic, aka Djikstra."""
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    priority_queue = [(0, ix) for ix in starting_nodes]
    min_cost = {ix: cost for cost, ix in priority_queue}

    while priority_queue:
        cost, ix = heappop(priority_queue)

        if ix == end_ix:
            break

        for ix_ in [(ix[0] + direction[0], ix[1] + direction[1]) for direction in directions]:
            if not (0 <= ix_[0] < mat.shape[0] and 0 <= ix_[1] < mat.shape[1]):
                continue
            if ord(mat[ix_[0], ix_[1]]) - ord(mat[ix[0], ix[1]]) > 1:
                continue

            new_path_length = cost + 1

            if ix_ in min_cost and min_cost[ix_] > new_path_length or ix_ not in min_cost:
                min_cost[ix_] = new_path_length
                heappush(priority_queue, (new_path_length, ix_))

    if end_ix != ix:
        return 9999

    return min_cost[ix]


def get_minimum_cost2(mat: np.ndarray, starting_nodes: list[tuple[int, int]], end_ix: tuple[int, int]) -> int:
    """This is BFS."""
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]
    value = 0
    edge_set = set(starting_nodes)
    visited = set()

    while edge_set:
        new_edge_set = set()
        for ix in edge_set:
            for ix_ in [(ix[0] + direction[0], ix[1] + direction[1]) for direction in directions]:
                if not (0 <= ix_[0] < mat.shape[0] and 0 <= ix_[1] < mat.shape[1]):
                    continue
                if ix_ in visited:
                    continue
                if ord(mat[ix_[0], ix_[1]]) - ord(mat[ix[0], ix[1]]) > 1:
                    continue
                if ix_ == end_ix:
                    return value + 1
                new_edge_set.add(ix_)
        visited.update(edge_set)
        edge_set = new_edge_set
        value += 1

    return -1


def print_path_lengths(mat: np.ndarray, best_cost: dict):
    t = np.empty(mat.shape, dtype=int)
    for i in range(mat.shape[0]):
        for j in range(mat.shape[1]):
            t[i, j] = best_cost.get((i, j), np.inf)
    np.set_printoptions(linewidth=400, infstr=".")
    print(t)


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    29
    """
    s = s.strip("\n")
    m = np.array([list(e) for e in s.splitlines()], dtype=str)
    start_ix = np.where(m == "S")
    end_ix = np.where(m == "E")
    m[start_ix] = "a"
    m[end_ix] = "z"
    start_pos_x, start_pos_y = np.where(m == "a")
    priority_queue = [(x, y) for x, y in zip(start_pos_x, start_pos_y)]
    return get_minimum_cost(m, priority_queue, (end_ix[0][0], end_ix[1][0]))


test_string = """
Sabqponm
abcryxxl
accszExk
acctuvwj
abdefghi
"""
solve_a(test_string)

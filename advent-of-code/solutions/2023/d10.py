# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""10. Pipe Maze https://adventofcode.com/2023/day/10"""
# Alternative approach: d10-raycast.py

import sys
import time
from collections import defaultdict


def part_a(s: str) -> int:
    grid = [list(x) for x in s.strip("\n").splitlines()]
    m, n = len(grid), len(grid[0])

    start_index = None
    for i in range(m):
        for j in range(n):
            if grid[i][j] == "S":
                start_index = (i, j)
                break
        if start_index:
            break

    graphs = []
    for c in ["-", "|", "F", "J", "L", "7"]:
        graph = defaultdict(list)
        grid[start_index[0]][start_index[1]] = c
        for i in range(m):
            for j in range(n):
                v = grid[i][j]
                left, right, up, down = (i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j)
                if v == "-":
                    if j >= 1 and grid[i][j - 1] in ["F", "L", "-"]:
                        graph[(i, j)].append(left)
                    if j < n - 1 and grid[i][j + 1] in ["7", "J", "-"]:
                        graph[(i, j)].append(right)
                elif v == "|":
                    if i >= 1 and grid[i - 1][j] in ["F", "7", "|"]:
                        graph[(i, j)].append(up)
                    if i < m - 1 and grid[i + 1][j] in ["J", "L", "|"]:
                        graph[(i, j)].append(down)
                elif v == "F":
                    if i < m - 1 and grid[i + 1][j] in ["J", "L", "|"]:
                        graph[(i, j)].append(down)
                    if j < n - 1 and grid[i][j + 1] in ["7", "J", "-"]:
                        graph[(i, j)].append(right)
                elif v == "J":
                    if i >= 1 and grid[i - 1][j] in ["F", "7", "|"]:
                        graph[(i, j)].append(up)
                    if j >= 1 and grid[i][j - 1] in ["F", "L", "-"]:
                        graph[(i, j)].append(left)
                elif v == "L":
                    if i >= 1 and grid[i - 1][j] in ["F", "7", "|"]:
                        graph[(i, j)].append(up)
                    if j < n - 1 and grid[i][j + 1] in ["7", "J", "-"]:
                        graph[(i, j)].append(right)
                elif v == "7":
                    if i < m - 1 and grid[i + 1][j] in ["J", "L", "|"]:
                        graph[(i, j)].append(down)
                    if j >= 1 and grid[i][j - 1] in ["F", "L", "-"]:
                        graph[(i, j)].append(left)
        graphs.append(graph)

    js = []
    for graph in graphs:
        j = 0
        seen = set()
        cur_queue = [start_index]
        next_queue = []
        borked_loop = False
        while cur_queue or next_queue:
            while cur_queue:
                x = cur_queue.pop()
                seen |= {x}
                if len(graph[x]) < 2:
                    borked_loop = True
                    break
                next_queue.extend(e for e in graph[x] if e not in seen)
            if borked_loop:
                break
            if not cur_queue and next_queue:
                cur_queue = next_queue.copy()
                next_queue = []
                j += 1
        if not borked_loop:
            js.append(j)

    return min(js)


def part_b(s: str) -> int:
    """
    Get the inner points of the polygon using the shoelace formula and Pick's
    theorem.

    """
    grid = [list(x) for x in s.strip("\n").splitlines()]
    m, n = len(grid), len(grid[0])

    start_index = None
    for i in range(m):
        for j in range(n):
            if grid[i][j] == "S":
                start_index = (i, j)
                break
        if start_index:
            break

    graphs = []
    symbols = ["-", "|", "F", "J", "L", "7"]
    for c in symbols:
        graph = defaultdict(list)
        grid[start_index[0]][start_index[1]] = c
        for i in range(m):
            for j in range(n):
                v = grid[i][j]
                left, right, up, down = (i, j - 1), (i, j + 1), (i - 1, j), (i + 1, j)
                if v == "-":
                    if j >= 1 and grid[i][j - 1] in ["F", "L", "-"]:
                        graph[(i, j)].append(left)
                    if j < n - 1 and grid[i][j + 1] in ["7", "J", "-"]:
                        graph[(i, j)].append(right)
                elif v == "|":
                    if i >= 1 and grid[i - 1][j] in ["F", "7", "|"]:
                        graph[(i, j)].append(up)
                    if i < m - 1 and grid[i + 1][j] in ["J", "L", "|"]:
                        graph[(i, j)].append(down)
                elif v == "F":
                    if i < m - 1 and grid[i + 1][j] in ["J", "L", "|"]:
                        graph[(i, j)].append(down)
                    if j < n - 1 and grid[i][j + 1] in ["7", "J", "-"]:
                        graph[(i, j)].append(right)
                elif v == "J":
                    if i >= 1 and grid[i - 1][j] in ["F", "7", "|"]:
                        graph[(i, j)].append(up)
                    if j >= 1 and grid[i][j - 1] in ["F", "L", "-"]:
                        graph[(i, j)].append(left)
                elif v == "L":
                    if i >= 1 and grid[i - 1][j] in ["F", "7", "|"]:
                        graph[(i, j)].append(up)
                    if j < n - 1 and grid[i][j + 1] in ["7", "J", "-"]:
                        graph[(i, j)].append(right)
                elif v == "7":
                    if i < m - 1 and grid[i + 1][j] in ["J", "L", "|"]:
                        graph[(i, j)].append(down)
                    if j >= 1 and grid[i][j - 1] in ["F", "L", "-"]:
                        graph[(i, j)].append(left)
        graphs.append(graph)

    cur_path = []
    for i, graph in enumerate(graphs):
        path = []
        visited = set()
        x = start_index
        while x not in visited:
            path.append(x)
            visited.add(x)
            if len(path) < 2:
                options = graph[x]
            else:
                options = [e for e in graph[x] if e != path[-2]]
            if not options:
                break
            x = options[0]
        if x != start_index:
            continue
        if len(path) > len(cur_path):
            cur_path = path

    return int(get_inner_points(path))


def get_inner_points(lst: list) -> float:
    """Get the points inside the area of an integer vertex polygon.

    The area of the polygon comes from the shoelace formula and the points
    inside from Pick's theorem.

    References:
    - https://en.wikipedia.org/wiki/Shoelace_formula
    - https://en.wikipedia.org/wiki/Pick%27s_theorem

    Examples:
    >>> get_inner_points(
    ...     [(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3), (2, 3), (1, 3), (0, 3), (0, 2), (0, 1), (0, 0)]
    ... )
    4.0
    >>> get_inner_points([(0, 0), (1, 0), (2, 0), (3, 0), (3, 1), (3, 2), (3, 3), (2, 2), (1, 1), (0, 0)])
    1.0
    """
    A = abs(sum(x[0] * y[1] - x[1] * y[0] for x, y in zip(lst, lst[1:] + [lst[0]]))) / 2
    b = len(set(lst))
    return A - b / 2 + 1


def print_path(seen: set, m: int, n: int):
    [print(x) for x in [["*" if (i, j) in seen else "." for j in range(m)] for i in range(n)]]


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

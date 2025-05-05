"""10. Pipe Maze https://adventofcode.com/2023/day/10"""

from collections import defaultdict


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    8
    >>> solve_a(test_string2)
    4
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


def solve_b(s: str, method: int = 0) -> int:
    """
    Method 0: Get the inner points of the polygon using the shoelace formula
    and Pick's theorem.
    Method 1: Get the inner points of the polygon using ray casting.

    Examples:
    >>> solve_b(test_string)
    1
    >>> solve_b(test_string2)
    1
    >>> solve_b(test_string3)
    4
    >>> solve_b(test_string4)
    4
    >>> solve_b(test_string5)
    8
    >>> solve_b(test_string6)
    10
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
    ix = 0
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
            ix = i

    if method == 0:
        return int(get_inner_points(path))

    grid[start_index[0]][start_index[1]] = symbols[ix]
    points = set(path)
    inner_points = set()
    for i in range(1, m - 1):
        inside = False
        horizontal = ""
        for j in range(n):
            if (i, j) not in points:
                grid[i][j] = "."
            if horizontal and grid[i][j] == "-":
                continue
            wall_condition = (
                grid[i][j] == "|" or horizontal == "F" and grid[i][j] == "J" or horizontal == "L" and grid[i][j] == "7"
            )
            if wall_condition:
                inside = not inside
                horizontal = ""
                continue
            if grid[i][j] in ["F", "L"]:
                horizontal = grid[i][j]
                continue
            if horizontal:
                horizontal = ""
                continue
            if inside:
                inner_points.add((i, j))

    return len(inner_points)


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


test_string = """
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
"""
test_string2 = """
.....
.S-7.
.|.|.
.L-J.
.....
"""
test_string3 = """
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
"""
test_string4 = """
..........
.S------7.
.|F----7|.
.||....||.
.||....||.
.|L-7F-J|.
.|..||..|.
.L--JL--J.
..........
"""
test_string5 = """
.F----7F7F7F7F-7....
.|F--7||||||||FJ....
.||.FJ||||||||L7....
FJL7L7LJLJ||LJ.L-7..
L--J.L7...LJS7F-7L7.
....F-J..F7FJ|L7L7L7
....L7.F7||L7|.L7L7|
.....|FJLJ|FJ|F7|.LJ
....FJL-7.||.||||...
....L---J.LJ.LJLJ...
"""
test_string6 = """
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
"""

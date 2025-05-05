"""6. https://adventofcode.com/2024/day/6

Part (b) is the interesting part. Initial solution ran in about 1.5s, but I left
many optimizations on the table. Turns out the bounds checking when moving the
guard forward took the most time. I removed some duplicate computations there,
which brought time down to 1s. Evin suggested compressing the grid to sorted
arrays of obstacles and using binary search to jump to the next obstacle
instead. That brought it down to 0.1s.
"""

from bisect import bisect_left, bisect_right, insort


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    41
    """
    s = s.strip("\n")
    grid = [list(row) for row in s.split("\n")]
    m, n = len(grid), len(grid[0])

    pos = None
    for i in range(m):
        for j in range(n):
            if grid[i][j] == "^":
                pos = (i, j)
                break
        if pos:
            break
    grid[pos[0]][pos[1]] = "."

    visited = set()
    d = (-1, 0)
    while 0 <= pos[0] + d[0] < m and 0 <= pos[1] + d[1] < n:
        if grid[pos[0] + d[0]][pos[1] + d[1]] == "#":
            match d:
                case (-1, 0):
                    d = (0, 1)
                case (0, 1):
                    d = (1, 0)
                case (1, 0):
                    d = (0, -1)
                case (0, -1):
                    d = (-1, 0)
        else:
            pos = (pos[0] + d[0], pos[1] + d[1])
            visited.add(pos)
    return len(visited)


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    6
    """
    s = s.strip("\n")
    grid = [list(row) for row in s.split("\n")]
    m, n = len(grid), len(grid[0])

    start_pos = None
    for i in range(m):
        for j in range(n):
            if grid[i][j] == "^":
                start_pos = (i, j)
                break
        if start_pos:
            break
    grid[start_pos[0]][start_pos[1]] = "."

    visited = set()
    d = (-1, 0)
    pos = start_pos
    while 0 <= pos[0] + d[0] < m and 0 <= pos[1] + d[1] < n:
        if grid[pos[0] + d[0]][pos[1] + d[1]] == "#":
            match d:
                case (-1, 0):
                    d = (0, 1)
                case (0, 1):
                    d = (1, 0)
                case (1, 0):
                    d = (0, -1)
                case (0, -1):
                    d = (-1, 0)
        else:
            pos = (pos[0] + d[0], pos[1] + d[1])
            visited.add(pos)
    visited.remove(start_pos)

    # Compress the grid to just the obstacles
    obstacles = {(i, j) for i in range(m) for j in range(n) if grid[i][j] == "#"}
    xs = [sorted([x for x in obstacles if x[1] == i], key=lambda x: x[0]) for i in range(n)]
    ys = [sorted([y for y in obstacles if y[0] == i], key=lambda y: y[1]) for i in range(m)]

    def get_next_obstacle(pos: tuple[int, int], d: tuple[int, int]) -> tuple[tuple[int, int], tuple[int, int]]:
        match d:
            case (-1, 0):
                row = pos[0]
                col = pos[1]
                idx = bisect_left(xs[col], (row, col))
                if idx > 0:
                    obstacle = xs[col][idx - 1]
                    return (obstacle[0] + 1, obstacle[1]), obstacle, (0, 1)
            case (0, 1):
                row = pos[0]
                col = pos[1]
                idx = bisect_right(ys[row], (row, col))
                if idx < len(ys[row]):
                    obstacle = ys[row][idx]
                    return (obstacle[0], obstacle[1] - 1), obstacle, (1, 0)
            case (1, 0):
                row = pos[0]
                col = pos[1]
                idx = bisect_right(xs[col], (row, col))
                if idx < len(xs[col]):
                    obstacle = xs[col][idx]
                    return (obstacle[0] - 1, obstacle[1]), obstacle, (0, -1)
            case (0, -1):
                row = pos[0]
                col = pos[1]
                idx = bisect_left(ys[row], (row, col))
                if idx > 0:
                    obstacle = ys[row][idx - 1]
                    return (obstacle[0], obstacle[1] + 1), obstacle, (-1, 0)
        return None, None, None

    total = 0
    for change_pos in visited:
        if grid[change_pos[0]][change_pos[1]] == "#":
            continue
        d = (-1, 0)
        obstacles.add(change_pos)
        insort(xs[change_pos[1]], change_pos, key=lambda x: x[0])
        insort(ys[change_pos[0]], change_pos, key=lambda y: y[1])
        pos, obstacle, d = get_next_obstacle(start_pos, d)
        visited_obstacles = set()
        while pos and (pos, obstacle) not in visited_obstacles:
            visited_obstacles.add((pos, obstacle))
            pos, obstacle, d = get_next_obstacle(pos, d)
        if (pos, obstacle) in visited_obstacles:
            total += 1
        obstacles.remove(change_pos)
        xs[change_pos[1]].remove(change_pos)
        ys[change_pos[0]].remove(change_pos)

    return total


def solve_b_slow(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    6
    """
    s = s.strip("\n")
    grid = [list(row) for row in s.split("\n")]
    m, n = len(grid), len(grid[0])

    start_pos = None
    for i in range(m):
        for j in range(n):
            if grid[i][j] == "^":
                start_pos = (i, j)
                break
        if start_pos:
            break
    grid[start_pos[0]][start_pos[1]] = "."

    visited = set()
    d = (-1, 0)
    pos = start_pos
    while 0 <= pos[0] + d[0] < m and 0 <= pos[1] + d[1] < n:
        if grid[pos[0] + d[0]][pos[1] + d[1]] == "#":
            match d:
                case (-1, 0):
                    d = (0, 1)
                case (0, 1):
                    d = (1, 0)
                case (1, 0):
                    d = (0, -1)
                case (0, -1):
                    d = (-1, 0)
        else:
            pos = (pos[0] + d[0], pos[1] + d[1])
            visited.add(pos)
    visited.remove(start_pos)

    total = 0
    for change_pos in visited:
        if grid[change_pos[0]][change_pos[1]] == "#":
            continue
        grid[change_pos[0]][change_pos[1]] = "#"
        pos = start_pos
        visited_obstacles = set()
        d = (-1, 0)
        loop = False
        next_pos = (pos[0] + d[0], pos[1] + d[1])
        while 0 <= next_pos[0] < m and 0 <= next_pos[1] < n:
            if grid[next_pos[0]][next_pos[1]] == "#":
                pos_dir = (pos[0], pos[1], next_pos[0], next_pos[1])
                if pos_dir in visited_obstacles:
                    loop = True
                    break
                visited_obstacles.add(pos_dir)
                match d:
                    case (-1, 0):
                        d = (0, 1)
                    case (0, 1):
                        d = (1, 0)
                    case (1, 0):
                        d = (0, -1)
                    case (0, -1):
                        d = (-1, 0)
            else:
                pos = next_pos
            next_pos = (pos[0] + d[0], pos[1] + d[1])
        if loop:
            total += 1
        grid[change_pos[0]][change_pos[1]] = "."

    return total


test_string = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

"""15. https://adventofcode.com/2024/day/15"""

import numpy as np


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string_a)
    2028
    """
    grid_str, path = s.strip().split("\n\n")
    grid_lines = grid_str.strip().split("\n")
    grid = np.array([list(line) for line in grid_lines])
    path = path.strip().replace("\n", "")
    m, n = grid.shape

    # Find start position
    pos = np.where(grid == "@")
    cur = (int(pos[0][0]), int(pos[1][0]))

    # Direction mappings
    dirs = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}

    for direction in path:
        dir_vec = dirs[direction]
        cur_ = cur

        # Follow a direction until we find an empty space or a wall
        while True:
            cur_ = (cur_[0] + dir_vec[0], cur_[1] + dir_vec[1])
            if grid[cur_[0], cur_[1]] == "#":
                break
            if grid[cur_[0], cur_[1]] == ".":
                break

        # If we don't see an empty space, then the boxes can't move
        if grid[cur_[0], cur_[1]] == "#":
            continue

        # Figure out if we're moving horizontally or vertically
        if dir_vec[0] == 0:
            xf = cur[0]
            ymin, ymax = min(cur[1], cur_[1]), max(cur[1], cur_[1])
            # Horizontal movement - shift the row
            row = grid[xf, ymin : ymax + 1]
            shifted_row = np.roll(row, dir_vec[1])
            grid[xf, ymin : ymax + 1] = shifted_row
        else:
            yf = cur[1]
            xmin, xmax = min(cur[0], cur_[0]), max(cur[0], cur_[0])
            # Vertical movement - shift the column
            col = grid[xmin : xmax + 1, yf]
            shifted_col = np.roll(col, dir_vec[0])
            grid[xmin : xmax + 1, yf] = shifted_col

        # Update the current position
        cur = (cur[0] + dir_vec[0], cur[1] + dir_vec[1])

    return sum(i * 100 + j for i in range(m) for j in range(n) if grid[i, j] == "O")


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string_b)
    9021
    """
    # Boxes are now extra wide, widen everything.
    s = s.replace("#", "##").replace(".", "..").replace("@", "@.").replace("O", "[]")
    grid_str, path = s.strip().split("\n\n")
    grid_lines = grid_str.strip().split("\n")
    grid = np.array([list(line) for line in grid_lines])
    path = path.strip().replace("\n", "")
    m, n = grid.shape

    # Find start position
    pos = np.where(grid == "@")
    cur = (int(pos[0][0]), int(pos[1][0]))

    # Direction mappings
    dirs = {">": (0, 1), "<": (0, -1), "^": (-1, 0), "v": (1, 0)}

    for direction in path:
        dir_vec = dirs[direction]

        # Find affected positions using BFS
        affected = list(bfs(grid, cur, dir_vec))

        # Empty if we can't move in this direction
        if not affected:
            continue

        # Sort affected by negative of direction to move furthest first
        affected.sort(key=lambda x: -dir_vec[0] * x[0] - dir_vec[1] * x[1])

        for pos in affected:
            # Swap element with the one in the direction of movement
            pos_ = (pos[0] + dir_vec[0], pos[1] + dir_vec[1])
            temp = grid[pos_[0], pos_[1]]
            grid[pos_[0], pos_[1]] = grid[pos[0], pos[1]]
            grid[pos[0], pos[1]] = temp

        # Update the current position
        cur = (cur[0] + dir_vec[0], cur[1] + dir_vec[1])

    # Calculate score - only count '[' characters
    return sum(i * 100 + j for i in range(m) for j in range(n) if grid[i, j] == "[")


def bfs(grid: np.ndarray, start: tuple[int, int], direction: tuple[int, int]) -> set[tuple[int, int]]:
    """Breadth-first search to find affected positions."""
    explored = set()
    unexplored = {start}

    while unexplored:
        cur = unexplored.pop()
        cur_ = (cur[0] + direction[0], cur[1] + direction[1])

        if grid[cur_[0], cur_[1]] == "#":
            return set()

        if grid[cur_[0], cur_[1]] == "[":
            if direction[0] == 0:  # moving right-left
                unexplored.add(cur_)
            else:
                unexplored.add(cur_)
                unexplored.add((cur_[0], cur_[1] + 1))

        if grid[cur_[0], cur_[1]] == "]":
            if direction[0] == 0:  # moving right-left
                unexplored.add(cur_)
            else:
                unexplored.add(cur_)
                unexplored.add((cur_[0], cur_[1] - 1))

        explored.add(cur)

    return explored


test_string_a = """
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
"""

test_string_b = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""

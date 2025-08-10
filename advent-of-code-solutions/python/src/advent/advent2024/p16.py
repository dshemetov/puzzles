"""16. https://adventofcode.com/2024/day/16"""

import heapq

# Direction vectors: east, south, west, north
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    7036
    """
    s = s.strip("\n")
    lines = s.split("\n")
    m, n = len(lines), len(lines[0])

    # Find start/end positions
    grid = []
    start_pos = (0, 0)
    end_pos = (0, 0)
    for i, line in enumerate(lines):
        grid.append([])
        for j, char in enumerate(line):
            grid[i].append(char)
            if char == "S":
                start_pos = (i, j)
            elif char == "E":
                end_pos = (i, j)

    # 3D cost array: (i, j, direction) -> cost
    costs = [[[float("inf")] * 4 for _ in range(n)] for _ in range(m)]
    costs[start_pos[0]][start_pos[1]][1] = 0  # Start facing east (direction 1)

    # Priority queue: (cost + heuristic, i, j, direction)
    queue = [(0, start_pos[0], start_pos[1], 1)]
    visited = set()

    while queue:
        current_cost, i, j, dir = heapq.heappop(queue)
        state = (i, j, dir)

        if state in visited:
            continue
        visited.add(state)

        if (i, j) == end_pos:
            return int(current_cost)

        # Try all 4 directions
        for new_dir in range(4):
            di, dj = DIRS[new_dir]
            ni, nj = i + di, j + dj

            # Check bounds and walls
            if ni < 0 or ni >= m or nj < 0 or nj >= n or grid[ni][nj] == "#":
                continue

            # Calculate cost (1000 for turns, 1 for movement)
            turn_cost = 1000 if dir != new_dir else 0
            new_cost = costs[i][j][dir] + 1 + turn_cost

            if new_cost < costs[ni][nj][new_dir]:
                costs[ni][nj][new_dir] = new_cost
                # Add Manhattan distance heuristic
                h = abs(ni - end_pos[0]) + abs(nj - end_pos[1])
                heapq.heappush(queue, (new_cost + h, ni, nj, new_dir))

    return -1  # No path found, should never happen


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    45
    """
    s = s.strip("\n")
    lines = s.split("\n")
    m, n = len(lines), len(lines[0])

    # Parse grid and find start/end positions
    grid = []
    start_pos = (0, 0)
    end_pos = (0, 0)
    for i, line in enumerate(lines):
        grid.append([])
        for j, char in enumerate(line):
            grid[i].append(char)
            if char == "S":
                start_pos = (i, j)
            elif char == "E":
                end_pos = (i, j)

    # 3D cost array: (i, j, direction) -> cost
    costs = [[[float("inf")] * 4 for _ in range(n)] for _ in range(m)]
    costs[start_pos[0]][start_pos[1]][1] = 0

    # Track predecessors for each state
    predecessors: dict[tuple[int, int, int], list[tuple[int, int, int]]] = {}
    predecessors[(start_pos[0], start_pos[1], 1)] = []

    # Priority queue for Dijkstra's algorithm
    queue = [(0, start_pos[0], start_pos[1], 1)]

    while queue:
        current_cost, i, j, dir = heapq.heappop(queue)

        # Try all 4 directions
        for new_dir in range(4):
            di, dj = DIRS[new_dir]
            ni, nj = i + di, j + dj

            # Check bounds and walls
            if ni < 0 or ni >= m or nj < 0 or nj >= n or grid[ni][nj] == "#":
                continue

            # Calculate cost
            turn_cost = 1000 if dir != new_dir else 0
            new_cost = costs[i][j][dir] + 1 + turn_cost
            new_state = (ni, nj, new_dir)

            if new_cost < costs[ni][nj][new_dir]:
                # Found better path
                costs[ni][nj][new_dir] = new_cost
                predecessors[new_state] = [(i, j, dir)]

                h = abs(ni - end_pos[0]) + abs(nj - end_pos[1])
                heapq.heappush(queue, (new_cost + h, ni, nj, new_dir))

            elif new_cost == costs[ni][nj][new_dir]:
                # Found equally good path
                if new_state in predecessors:
                    predecessors[new_state].append((i, j, dir))
                else:
                    predecessors[new_state] = [(i, j, dir)]

    # Find minimum cost to reach end
    min_end_cost = min(costs[end_pos[0]][end_pos[1]])

    # Backtrack from all optimal end states
    on_optimal_path = [[False] * n for _ in range(m)]
    queue_back = []
    visited_states = set()
    # Initialize queue
    for dir in range(4):
        if costs[end_pos[0]][end_pos[1]][dir] == min_end_cost:
            state = (end_pos[0], end_pos[1], dir)
            queue_back.append(state)
            visited_states.add(state)

    while queue_back:
        state = queue_back.pop()
        i, j, dir = state
        on_optimal_path[i][j] = True

        if state in predecessors:
            for pred_state in predecessors[state]:
                if pred_state not in visited_states:
                    visited_states.add(pred_state)
                    queue_back.append(pred_state)

    return sum(sum(row) for row in on_optimal_path)


test_string = """###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############"""

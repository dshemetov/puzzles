# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""18. https://adventofcode.com/2024/day/18"""

import ast
import heapq
import inspect
import sys
import time


def solve_maze(grid: list[list[str]], n: int, m: int) -> tuple[int, list[tuple[int, int]]]:
    # Priority queue: (cost, position)
    queue = [(0, (1, 1))]
    heapq.heapify(queue)

    # Cost matrix: -1 means unvisited (1-indexed like Julia)
    costs = [[-1 for _ in range(m + 1)] for _ in range(n + 1)]
    costs[1][1] = 0

    # For path reconstruction
    came_from = [[None for _ in range(m + 1)] for _ in range(n + 1)]
    came_from[1][1] = None

    # Directions: right, down, up, left
    directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

    while queue:
        cost, pos = heapq.heappop(queue)
        x, y = pos

        # Check if we reached the destination (n, m)
        if pos == (n, m):
            # Reconstruct path
            path = []
            current = pos
            while current is not None:
                path.append(current)
                current = came_from[current[0]][current[1]]
            return cost, list(reversed(path))

        # Skip if we found a better path to this position
        if cost > costs[x][y]:
            continue

        # Try all directions
        for dx, dy in directions:
            new_x, new_y = x + dx, y + dy

            # Check bounds (1-indexed)
            if not (1 <= new_x <= n and 1 <= new_y <= m):
                continue

            # Check if position is blocked
            if grid[new_x][new_y] == "#":
                continue

            new_cost = cost + 1

            # Update if we found a better path
            if costs[new_x][new_y] == -1 or new_cost < costs[new_x][new_y]:
                costs[new_x][new_y] = new_cost
                came_from[new_x][new_y] = pos
                heapq.heappush(queue, (new_cost, (new_x, new_y)))

    return -1, []


def part_a(s: str, n: int = 71, m: int = 71, num_bytes: int = 1024) -> int:
    s = s.strip("\n")
    lines = s.split("\n")

    # Determine grid size and number of bytes based on input

    grid = [["." for _ in range(m + 1)] for _ in range(n + 1)]

    # Add obstacles
    for line in lines[:num_bytes]:
        y, x = map(int, line.split(","))
        grid[x + 1][y + 1] = "#"

    # Find shortest path with Dijkstra
    cost, _path = solve_maze(grid, n, m)
    return cost


def part_b(s: str, n: int = 71, m: int = 71, num_bytes: int = 1024) -> str:
    s = s.strip("\n")
    lines = s.split("\n")

    grid = [["." for _ in range(m + 1)] for _ in range(n + 1)]

    # Add obstacles
    for line in lines[:num_bytes]:
        y, x = map(int, line.split(","))
        grid[x + 1][y + 1] = "#"

    # Find initial path
    cost, path = solve_maze(grid, n, m)

    # Add obstacles one by one and check if path becomes impossible
    i = num_bytes
    while cost != -1 and i < len(lines):
        i += 1
        y, x = map(int, lines[i - 1].split(","))
        grid[x + 1][y + 1] = "#"

        # Only recalculate if the new obstacle is on our current path
        if (x + 1, y + 1) in path:
            cost, path = solve_maze(grid, n, m)

    if cost == -1:
        return lines[i - 1]
    return "-1"


# Test string from Julia solution


def params_for(part, extra: list[str]) -> dict:
    """The key=value arguments after the input file that this part declares as keyword parameters."""
    pairs = [arg.split("=", 1) for arg in extra]
    wanted = inspect.signature(part).parameters
    return {k: ast.literal_eval(v) for k, v in pairs if k in wanted}


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s, **params_for(part, sys.argv[2:])))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

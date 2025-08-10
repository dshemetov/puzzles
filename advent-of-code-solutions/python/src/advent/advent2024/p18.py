"""18. https://adventofcode.com/2024/day/18"""

import heapq


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


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string_18)
    22
    """
    s = s.strip("\n")
    lines = s.split("\n")

    # Determine grid size and number of bytes based on input
    if not s or s == test_string_18.strip("\n"):
        n, m = 7, 7
        num_bytes = 12
    else:
        n, m = 71, 71
        num_bytes = 1024

    grid = [["." for _ in range(m + 1)] for _ in range(n + 1)]

    # Add obstacles
    for line in lines[:num_bytes]:
        y, x = map(int, line.split(","))
        grid[x + 1][y + 1] = "#"

    # Find shortest path with Dijkstra
    cost, path = solve_maze(grid, n, m)
    return cost


def solve_b(s: str) -> str:
    """
    Examples:
    >>> solve_b(test_string_18)
    '6,1'
    """
    s = s.strip("\n")
    lines = s.split("\n")

    if not s or s == test_string_18.strip("\n"):
        n, m = 7, 7
        num_bytes = 12
    else:
        n, m = 71, 71
        num_bytes = 1024

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
test_string_18 = """5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""


if __name__ == "__main__":
    print("Testing Part A:")
    result_a = solve_a(test_string_18)
    print(f"Part A result: {result_a}")
    print("Expected: 22")
    print(f"Match: {result_a == 22}")

    print("\nTesting Part B:")
    result_b = solve_b(test_string_18)
    print(f"Part B result: {result_b}")
    print("Expected: 6,1")
    print(f"Match: {result_b == '6,1'}")

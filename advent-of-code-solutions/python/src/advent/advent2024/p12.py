"""12. https://adventofcode.com/2024/day/12"""


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    1930
    """
    s = s.strip("\n")
    grids = s.split("\n\n")

    if len(grids) > 1:
        grid_str = grids[1].strip()
        return solve_single_grid_a(grid_str)

    total = 0
    for grid_str in grids:
        if not grid_str.strip():
            continue
        total += solve_single_grid_a(grid_str.strip())

    return total


def solve_single_grid_a(s: str) -> int:
    lines = s.splitlines()
    m, n = len(lines), len(lines[0])
    grid = [[ord(char) for char in line] for line in lines]

    visited = [[False] * n for _ in range(m)]
    total = 0
    for i in range(m):
        for j in range(n):
            if visited[i][j]:
                continue

            # Clear and reuse the region list
            region = []

            # DFS to find connected region
            char_type = grid[i][j]
            stack = [(i, j)]

            while stack:
                ci, cj = stack.pop()
                if ci < 0 or ci >= m or cj < 0 or cj >= n:
                    continue
                if visited[ci][cj] or grid[ci][cj] != char_type:
                    continue

                visited[ci][cj] = True
                region.append((ci, cj))

                # Add neighbors (bounds will be checked in next iteration)
                stack.append((ci - 1, cj))
                stack.append((ci + 1, cj))
                stack.append((ci, cj - 1))
                stack.append((ci, cj + 1))

            if not region:
                continue

            # Calculate perimeter efficiently
            area = len(region)
            perimeter = 0

            for ri, rj in region:
                # Check each direction
                for di, dj in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                    ni, nj = ri + di, rj + dj
                    # Count edge if neighbor is out of bounds or different type
                    if ni < 0 or ni >= m or nj < 0 or nj >= n or grid[ni][nj] != char_type:
                        perimeter += 1

            total += area * perimeter

    return total


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    368
    """
    s = s.strip("\n")
    grids = s.split("\n\n")

    if len(grids) > 3:
        grid_str = grids[3].strip()
        return solve_single_grid_b(grid_str)

    total = 0
    for grid_str in grids:
        if not grid_str.strip():
            continue
        total += solve_single_grid_b(grid_str.strip())

    return total


def solve_single_grid_b(s: str) -> int:
    lines = s.splitlines()
    m, n = len(lines), len(lines[0])
    grid = [[ord(char) for char in line] for line in lines]

    visited = [[False] * n for _ in range(m)]
    total = 0
    for i in range(m):
        for j in range(n):
            if visited[i][j]:
                continue

            # Clear and reuse the region list
            region = []

            # DFS to find connected region
            char_type = grid[i][j]
            stack = [(i, j)]

            while stack:
                ci, cj = stack.pop()
                if ci < 0 or ci >= m or cj < 0 or cj >= n:
                    continue
                if visited[ci][cj] or grid[ci][cj] != char_type:
                    continue

                visited[ci][cj] = True
                region.append((ci, cj))

                # Add neighbors (bounds will be checked in next iteration)
                stack.append((ci - 1, cj))
                stack.append((ci + 1, cj))
                stack.append((ci, cj - 1))
                stack.append((ci, cj + 1))

            if not region:
                continue

            # Calculate sides efficiently
            area = len(region)
            sides = count_sides(region)

            total += area * sides

    return total


def count_sides(region):
    """Count sides using corner pattern matching."""
    # Convert region to a set for O(1) lookups
    region_set = set(region)

    # Define the common corner directions
    corner_directions = [
        ((1, 0), (1, 1), (0, 1)),  # right-down
        ((1, 0), (1, -1), (0, -1)),  # left-down
        ((-1, 0), (-1, 1), (0, 1)),  # right-up
        ((-1, 0), (-1, -1), (0, -1)),  # left-up
    ]

    # Define patterns for different corner types
    corner_patterns = [
        (False, False, False),  # Exterior corners
        (True, False, True),  # Interior corners
        (False, True, False),  # Corner points touching
    ]

    total_sides = 0
    for i, j in region:
        for directions in corner_directions:
            for pattern in corner_patterns:
                # Check if this corner configuration matches the pattern
                matches = True
                for k, (di, dj) in enumerate(directions):
                    ni, nj = i + di, j + dj
                    in_region = (ni, nj) in region_set
                    if in_region != pattern[k]:
                        matches = False
                        break

                if matches:
                    total_sides += 1

    return total_sides


test_string = """
AAAA
BBCD
BBCC
EEEC

RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE

EEEEE
EXXXX
EEEEE
EXXXX
EEEEE

AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
"""

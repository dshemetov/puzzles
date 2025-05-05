"""11. Cosmic Expansion https://adventofcode.com/2023/day/11"""

from itertools import combinations


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    374
    """
    grid = [list(line) for line in s.strip("\n").splitlines()]
    m, n = len(grid), len(grid[0])

    # Get empty rows and cols
    rows = [all(grid[i][j] == "." for j in range(n)) for i in range(m)]
    cols = [all(grid[i][j] == "." for i in range(m)) for j in range(n)]

    # Expand vertically
    grid2 = []
    for i in range(m):
        grid2.append(grid[i])
        if rows[i]:
            grid2.append(grid[i])

    # Expand horizontally
    grid3 = []
    for i in range(len(grid2)):
        grid3.append([])
        for j in range(n):
            grid3[i].append(grid2[i][j])
            if cols[j]:
                grid3[i].append(grid2[i][j])

    # Mark the locations of the #
    m, n = len(grid3), len(grid3[0])
    ixs = [(i, j) for i in range(m) for j in range(n) if grid3[i][j] == "#"]

    # Find distance between all pairs of #
    total = 0
    for ix, ix2 in combinations(ixs, r=2):
        total += abs(ix[0] - ix2[0]) + abs(ix[1] - ix2[1])
    return total


def solve_b(s: str, f: int = 10**6) -> int:
    """
    Examples:
    >>> solve_b(test_string, 10)
    1030
    >>> solve_b(test_string, 100)
    8410
    """
    s = s.strip("\n")
    grid = [list(line) for line in s.strip("\n").splitlines()]
    m, n = len(grid), len(grid[0])

    # Get empty rows and cols
    rows = [i for i in range(m) if all(grid[i][j] == "." for j in range(n))]
    cols = [j for j in range(n) if all(grid[i][j] == "." for i in range(m))]

    # Mark the locations of the #
    m, n = len(grid), len(grid[0])
    ixs = [(i, j) for i in range(m) for j in range(n) if grid[i][j] == "#"]

    # Find distance between all pairs of #
    total = 0
    for ix, ix2 in combinations(ixs, r=2):
        minx, maxx = min(ix[0], ix2[0]), max(ix[0], ix2[0])
        miny, maxy = min(ix[1], ix2[1]), max(ix[1], ix2[1])
        r1 = abs(ix[0] - ix2[0])
        r2 = sum(1 for x in rows if minx <= x <= maxx)
        c1 = abs(ix[1] - ix2[1])
        c2 = sum(1 for y in cols if miny <= y <= maxy)
        total += (r1 - r2) + (c1 - c2) + f * (r2 + c2)
    return total


test_string = """
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
"""

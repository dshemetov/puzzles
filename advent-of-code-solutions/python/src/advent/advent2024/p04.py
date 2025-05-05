"""4. https://adventofcode.com/2024/day/4"""


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    18
    """
    s = s.strip("\n")
    grid = [list(row) for row in s.split("\n")]
    m, n = len(grid), len(grid[0])
    total = 0
    word = "XMAS"
    for i in range(m):
        for j in range(n):
            for d in [(0, 1), (1, 0), (1, 1), (-1, 1)]:
                for sgn in [1, -1]:
                    match = True
                    for k in range(4):
                        x, y = i + sgn * k * d[0], j + sgn * k * d[1]
                        if x < 0 or y < 0 or x >= m or y >= n:
                            match = False
                            break
                        if grid[x][y] != word[k]:
                            match = False
                            break
                    if match:
                        total += 1
    return total


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    9
    """
    s = s.strip("\n")
    grid = [list(row) for row in s.split("\n")]
    m, n = len(grid), len(grid[0])
    total = 0
    word = list("MAS")
    rword = list(reversed(word))
    for i in range(1, m - 1):
        for j in range(1, n - 1):
            upright = [grid[i - k][j + k] for k in range(-1, 2) if 0 <= i - k < m and 0 <= j + k < n]
            downright = [grid[i + k][j + k] for k in range(-1, 2) if 0 <= i + k < m and 0 <= j + k < n]
            if upright in (word, rword) and downright in (word, rword):
                total += 1

    return total


test_string = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

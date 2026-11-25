def p1706(grid: list[list[int]]) -> list[int]:
    """1706. Where Will The Ball Fall https://leetcode.com/problems/where-will-the-ball-fall/

    Examples
    --------
    >>> p1706([[-1]])
    [-1]
    >>> p1706([[1, 1, 1, -1, -1], [1, 1, 1, -1, -1], [-1, -1, -1, 1, 1], [1, 1, 1, 1, -1], [-1, -1, -1, -1, -1]])
    [1, -1, -1, -1, -1]
    >>> p1706([[1, 1, 1, 1, 1, 1]])
    [1, 2, 3, 4, 5, -1]
    >>> p1706([[1, 1, 1, 1, 1, 1], [-1, -1, -1, -1, -1, -1], [1, 1, 1, 1, 1, 1], [-1, -1, -1, -1, -1, -1]])
    [0, 1, 2, 3, 4, -1]

    """

    def find_ball(i: int) -> int:
        x, y = 0, i
        while True:
            if grid[x][y] == 1:
                if y == len(grid[0]) - 1 or grid[x][y + 1] == -1:
                    return -1
                y += 1
            else:
                if y == 0 or grid[x][y - 1] == 1:
                    return -1
                y -= 1
            x += 1
            if x == len(grid):
                return y

    return [find_ball(i) for i in range(len(grid[0]))]

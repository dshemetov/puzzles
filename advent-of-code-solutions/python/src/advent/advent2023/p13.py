"""13. Point of Incidence https://adventofcode.com/2023/day/13"""


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    405
    """
    patterns = s.strip("\n").split("\n\n")
    total = 0
    for pattern in patterns:
        grid = [list(row) for row in pattern.split("\n")]
        m, n = len(grid), len(grid[0])

        # Check for reflection across a vertical in every row
        for v in range(1, n):
            all_ok = True
            for i in range(m):
                one_ok = True
                for k in range(min(v - 1, n - v - 1) + 1):
                    if grid[i][v - k - 1] != grid[i][v + k]:
                        one_ok = False
                        break
                if not one_ok:
                    all_ok = False
                    break
            if all_ok:
                break

        if all_ok:
            total += v
            continue

        # Check for reflection across a horizontal in every column
        for h in range(1, m):
            all_ok = True
            for j in range(n):
                one_ok = True
                for k in range(min(h - 1, m - h - 1) + 1):
                    if grid[h - k - 1][j] != grid[h + k][j]:
                        one_ok = False
                        break
                if not one_ok:
                    all_ok = False
                    break
            if all_ok:
                break

        if all_ok:
            total += h * 100

    return total


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    400
    """
    patterns = s.strip("\n").split("\n\n")
    total = 0
    for pattern in patterns:
        grid = [list(row) for row in pattern.split("\n")]
        m, n = len(grid), len(grid[0])

        prev_line = ["v", -1]
        # Check for reflection across a vertical in every row
        for v in range(1, n):
            all_ok = True
            for i in range(m):
                one_ok = True
                for k in range(min(v - 1, n - v - 1) + 1):
                    if grid[i][v - k - 1] != grid[i][v + k]:
                        one_ok = False
                        break
                if not one_ok:
                    all_ok = False
                    break
            if all_ok:
                break

        if all_ok:
            prev_line = ["v", v]

        # Check for reflection across a horizontal in every column
        for h in range(1, m):
            all_ok = True
            for j in range(n):
                one_ok = True
                for k in range(min(h - 1, m - h - 1) + 1):
                    if grid[h - k - 1][j] != grid[h + k][j]:
                        one_ok = False
                        break
                if not one_ok:
                    all_ok = False
                    break
            if all_ok:
                break

        if all_ok:
            prev_line = ["h", h]

        smudge_found = False
        for i_ in range(m):
            for j_ in range(n):
                # Change one grid cell
                if grid[i_][j_] == "#":
                    grid[i_][j_] = "."
                else:
                    grid[i_][j_] = "#"

                # Check for reflection across a vertical in every row
                for v in range(1, n):
                    all_ok = True
                    for i in range(m):
                        one_ok = True
                        for k in range(min(v - 1, n - v - 1) + 1):
                            if grid[i][v - k - 1] != grid[i][v + k]:
                                one_ok = False
                                break
                        if not one_ok:
                            all_ok = False
                            break
                    if all_ok and prev_line != ["v", v]:
                        break

                if all_ok and prev_line != ["v", v]:
                    smudge_found = True
                    total += v
                else:
                    # Check for reflection across a horizontal in every column
                    for h in range(1, m):
                        all_ok = True
                        for j in range(n):
                            one_ok = True
                            for k in range(min(h - 1, m - h - 1) + 1):
                                if grid[h - k - 1][j] != grid[h + k][j]:
                                    one_ok = False
                                    break
                            if not one_ok:
                                all_ok = False
                                break
                        if all_ok and prev_line != ["h", h]:
                            break

                    if all_ok and prev_line != ["h", h]:
                        total += h * 100
                        smudge_found = True

                if smudge_found:
                    break

                # Reset the grid
                if grid[i_][j_] == "#":
                    grid[i_][j_] = "."
                else:
                    grid[i_][j_] = "#"
            if smudge_found:
                break

    return total


test_string = """
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
"""

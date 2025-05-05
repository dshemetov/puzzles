"""Crossed Wires
https://adventofcode.com/2019/day/3
"""


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    159
    """
    a, b = s.strip("\n").split("\n")
    a, b = a.split(","), b.split(",")
    a_visited, b_visited = set(), set()
    a_cur, b_cur = (0, 0), (0, 0)

    for t in a:
        if t[0] == "R":
            for _ in range(int(t[1:])):
                a_cur = (a_cur[0] + 1, a_cur[1])
                a_visited.add(a_cur)
        elif t[0] == "L":
            for _ in range(int(t[1:])):
                a_cur = (a_cur[0] - 1, a_cur[1])
                a_visited.add(a_cur)
        elif t[0] == "U":
            for _ in range(int(t[1:])):
                a_cur = (a_cur[0], a_cur[1] + 1)
                a_visited.add(a_cur)
        elif t[0] == "D":
            for _ in range(int(t[1:])):
                a_cur = (a_cur[0], a_cur[1] - 1)
                a_visited.add(a_cur)

    for t in b:
        if t[0] == "R":
            for _ in range(int(t[1:])):
                b_cur = (b_cur[0] + 1, b_cur[1])
                b_visited.add(b_cur)
        elif t[0] == "L":
            for _ in range(int(t[1:])):
                b_cur = (b_cur[0] - 1, b_cur[1])
                b_visited.add(b_cur)
        elif t[0] == "U":
            for _ in range(int(t[1:])):
                b_cur = (b_cur[0], b_cur[1] + 1)
                b_visited.add(b_cur)
        elif t[0] == "D":
            for _ in range(int(t[1:])):
                b_cur = (b_cur[0], b_cur[1] - 1)
                b_visited.add(b_cur)

    m = float("inf")
    for x, y in a_visited.intersection(b_visited):
        m = min(m, abs(x) + abs(y))

    return m


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    610
    """
    a, b = s.strip("\n").split("\n")
    a, b = a.split(","), b.split(",")
    a_path, b_path = [], []
    a_cur, b_cur = (0, 0), (0, 0)

    for t in a:
        if t[0] == "R":
            for _ in range(int(t[1:])):
                a_cur = (a_cur[0] + 1, a_cur[1])
                a_path.append(a_cur)
        elif t[0] == "L":
            for _ in range(int(t[1:])):
                a_cur = (a_cur[0] - 1, a_cur[1])
                a_path.append(a_cur)
        elif t[0] == "U":
            for _ in range(int(t[1:])):
                a_cur = (a_cur[0], a_cur[1] + 1)
                a_path.append(a_cur)
        elif t[0] == "D":
            for _ in range(int(t[1:])):
                a_cur = (a_cur[0], a_cur[1] - 1)
                a_path.append(a_cur)

    for t in b:
        if t[0] == "R":
            for _ in range(int(t[1:])):
                b_cur = (b_cur[0] + 1, b_cur[1])
                b_path.append(b_cur)
        elif t[0] == "L":
            for _ in range(int(t[1:])):
                b_cur = (b_cur[0] - 1, b_cur[1])
                b_path.append(b_cur)
        elif t[0] == "U":
            for _ in range(int(t[1:])):
                b_cur = (b_cur[0], b_cur[1] + 1)
                b_path.append(b_cur)
        elif t[0] == "D":
            for _ in range(int(t[1:])):
                b_cur = (b_cur[0], b_cur[1] - 1)
                b_path.append(b_cur)

    m = float("inf")
    for x, y in set(a_path).intersection(set(b_path)):
        m = min(m, a_path.index((x, y)) + b_path.index((x, y)) + 2)

    return m


test_string = """
R75,D30,R83,U83,L12,D49,R71,U7,L72
U62,R66,U55,R34,D71,R55,D58,R83
"""

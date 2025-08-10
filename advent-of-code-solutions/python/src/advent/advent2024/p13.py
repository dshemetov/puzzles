"""13. https://adventofcode.com/2024/day/13"""

import re


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    480
    """
    s = s.strip("\n")
    machines = s.split("\n\n")

    total = 0
    for machine in machines:
        line_a, line_b, prize = machine.split("\n")
        button_a = [int(x) for x in re.findall(r"\d+", line_a)]
        button_b = [int(x) for x in re.findall(r"\d+", line_b)]
        prize = [int(x) for x in re.findall(r"\d+", prize)]

        # Set up the system Ax = b
        a11, a12 = button_a[0], button_b[0]
        a21, a22 = button_a[1], button_b[1]
        b1, b2 = prize[0], prize[1]
        det = a11 * a22 - a12 * a21

        solution = None
        if det != 0:
            # Solve x = A^(-1) * b
            x1 = (a22 * b1 - a12 * b2) / det
            x2 = (a11 * b2 - a21 * b1) / det
            if x1 >= 0 and x2 >= 0 and x1.is_integer() and x2.is_integer():
                solution = [int(x1), int(x2)]
        else:
            # Matrix is singular - check if point lies on the line
            j = b1 / a11
            if j.is_integer() and j >= 0 and j * a12 == b2:
                solution = [0, int(j)]

        if solution is not None and all(x <= 100 for x in solution):
            total += 3 * solution[0] + solution[1]

    return int(total)


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    875318608908
    """
    s = s.strip("\n")
    machines = s.split("\n\n")

    total = 0
    offset = 10_000_000_000_000
    for machine in machines:
        line_a, line_b, prize = machine.split("\n")
        button_a = [int(x) for x in re.findall(r"\d+", line_a)]
        button_b = [int(x) for x in re.findall(r"\d+", line_b)]
        prize = [int(x) for x in re.findall(r"\d+", prize)]

        # Set up the system Ax = b, this time with offset
        a11, a12 = button_a[0], button_b[0]
        a21, a22 = button_a[1], button_b[1]
        b1, b2 = prize[0] + offset, prize[1] + offset

        solution = None
        det = a11 * a22 - a12 * a21
        if det != 0:
            # x = A^(-1) * b
            x1 = (a22 * b1 - a12 * b2) / det
            x2 = (a11 * b2 - a21 * b1) / det

            # Check if solution is valid (non-negative integers)
            if x1 >= 0 and x2 >= 0 and x1.is_integer() and x2.is_integer():
                solution = [int(x1), int(x2)]
        else:
            # Try using only button B
            j = prize[0] / button_b[0]
            if j.is_integer() and j >= 0 and j * button_b[1] == prize[1]:
                solution = [0, int(j)]

        # If we found a valid solution, calculate cost
        if solution is not None:
            total += 3 * solution[0] + solution[1]

    return total


test_string = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

"""Trick Shot
https://adventofcode.com/2021/day/17
"""

import re


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    45
    """
    xmin, xmax, ymin, ymax = [int(x) for x in re.findall(r"(-*\d+)", s)]
    min_vx, max_vx = valid_vxs(xmin, xmax)
    min_vy, max_vy = valid_vys(ymin, ymax)
    max_y = -float("inf")
    for vy in range(min_vy, max_vy):
        for vx in range(min_vx, max_vx):
            valid, potent_max_y = ends_in_target(vx, vy, xmin, xmax, ymin, ymax)
            if valid:
                if potent_max_y > max_y:
                    max_y = potent_max_y

    return max_y


def valid_vxs(xmin, xmax) -> tuple[int, int]:
    vx = 0
    for vx in range(xmin + 1):
        x = vx * (vx + 1) / 2
        if xmin < x < xmax:
            min_vx = vx
            break

    max_vx = xmax + 1  # guaranteed to be too fast
    return (min_vx - 1, max_vx)


def valid_vys(ymin, ymax):
    return ymin, max(abs(ymin), abs(ymax)) + 2


def ends_in_target(vx_: int, vy_: int, xmin, xmax, ymin, ymax) -> tuple[bool, int]:
    vx, vy = vx_, vy_
    impossibru = False
    x, y = 0, 0
    max_y = -float("inf")
    while not impossibru:
        x += vx
        y += vy

        max_y = max(max_y, y)
        if xmin <= x <= xmax and ymin <= y <= ymax:
            return True, max_y

        vx = max(vx - 1, 0)
        vy -= 1

        if x > xmax or y < ymin:
            # print("Its impossibru!!!!")
            impossibru = True
    return False, max_y


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    112
    """
    xmin, xmax, ymin, ymax = [int(x) for x in re.findall(r"(-*\d+)", s)]
    min_vx, max_vx = valid_vxs(xmin, xmax)
    min_vy, max_vy = valid_vys(ymin, ymax)
    valid_vxvys = 0
    for vy in range(min_vy, max_vy):
        for vx in range(min_vx, max_vx):
            valid, _ = ends_in_target(vx, vy, xmin, xmax, ymin, ymax)
            if valid:
                valid_vxvys += 1

    return valid_vxvys


test_string = """target area: x=20..30, y=-10..-5"""

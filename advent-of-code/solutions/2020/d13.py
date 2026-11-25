# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""https://adventofcode.com/2020/day/13"""

import sys
import time
from itertools import product


def get_gcd(a: int, b: int) -> int:
    """Euclidean algorithm greatest common divisor.

    Returns the largest integer d such that d | a and d | b.

    Examples:
    >>> get_gcd(6, 4)
    2
    >>> get_gcd(4, 6)
    2
    >>> get_gcd(5, 17)
    1
    """
    r, r_ = a, b
    while r_ > 0:
        r, r_ = r_, r % r_
    return r


def get_bezout_coefficients(a: int, b: int) -> tuple[int, int]:
    """Extended Euclidean algorithm.

    Returns integer coefficients x and y such that x * a + y * b = gcd(a, b).

    Examples:
    >>> get_bezout_coefficients(6, 4)
    (1, -1)
    >>> get_bezout_coefficients(4, 6)
    (-1, 1)
    >>> get_bezout_coefficients(5, 17)
    (7, -2)
    """
    s, s_ = 0, 1
    t, t_ = 1, 0
    r, r_ = a, b
    while r_ > 0:
        q = r // r_
        r, r_ = r_, r - q * r_
        s, s_ = s_, s - q * s_
        t, t_ = t_, t - q * t_
    return (t, s)


def part_a(s: str) -> int:
    depart_time, bus_schedule = s.split("\n")
    depart_time, bus_schedule = int(depart_time), filter(lambda x: x != "x", bus_schedule.split(","))
    bus_id, next_bus_time = min(
        [(int(bus_id), get_next_bus_time(depart_time, int(bus_id))) for bus_id in bus_schedule],
        key=lambda x: x[1],
    )
    return bus_id * (next_bus_time - depart_time)


def get_next_bus_time(time: int, period: int) -> int:
    return time + get_minutes_until_next_bus(time, period)


def get_minutes_until_next_bus(time: int, period: int) -> int:
    if time % period == 0:
        return 0
    else:
        return period - time % period


def part_b(s: str) -> int:
    _, bus_schedule = s.split("\n")
    bus_schedule: list[tuple[int, int]] = [
        (-offset, int(bus_id)) for offset, bus_id in enumerate(bus_schedule.split(",")) if bus_id != "x"
    ]
    return solve_modular_congruence_equations(bus_schedule)


def solve_modular_congruence_equations(residue_classes: list[tuple[int, int]]) -> int:
    """Solve an arbitrary system of modular equations.

    Elements in residue_classes are assumed to be pairs (a_i, b_i) and the system of equations to solve is:
        x = a_i mod b_i,          i = 1, 2, ...
    """
    if not all(get_gcd(a, b) == 1 for a, b in product((m for _, m in residue_classes), repeat=2) if a != b):
        raise ValueError("The moduli in the system are not all pair-wise relatively prime.")

    residue_classes_ = residue_classes.copy()
    while len(residue_classes_) > 1:
        bus1, bus2 = residue_classes_.pop(), residue_classes_.pop()
        a, b = solve_modular_congruence_equation_pair(bus1, bus2)
        residue_classes_ += [(a, b)]
    return a


def solve_modular_congruence_equation_pair(b1: tuple[int, int], b2: tuple[int, int]) -> tuple[int, int]:
    """Solve a system of two modular equations.

    Solves the system
        x = a1 mod n1
        x = a2 mod n2
    where a1, n1 = b1 and a2, n2 = b2.
    """
    (a1, n1), (a2, n2) = b1, b2
    s, t = get_bezout_coefficients(n1, n2)
    x = a2 * s * n1 + a1 * t * n2
    return (x % (n1 * n2), n1 * n2)


test_strings = [
    """939\n7,13,x,x,59,x,31,19""",
    """1\n17,x,13,19""",
    """1\n67,7,59,61""",
    """1\n67,x,7,59,61""",
    """1\n67,7,x,59,61""",
    """1\n1789,37,47,1889""",
]


def test_get_next_bus_time():
    assert get_next_bus_time(14, 7) == 14
    assert get_next_bus_time(15, 7) == 21
    assert get_next_bus_time(36, 11) == 44


def test_part_a():
    assert part_a(test_strings[0]) == 295


def test_solve_modular_congruence_equation_pair():
    assert solve_modular_congruence_equation_pair((2, 5), (3, 7)) == (17, 35)
    assert solve_modular_congruence_equation_pair((2, 5), (3, 7)) == (17, 35)


def test_part_b():
    assert part_b(test_strings[0]) == 1068781
    assert part_b(test_strings[1]) == 3417
    assert part_b(test_strings[2]) == 754018
    assert part_b(test_strings[3]) == 779210
    assert part_b(test_strings[4]) == 1261476
    assert part_b(test_strings[5]) == 1202161486


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

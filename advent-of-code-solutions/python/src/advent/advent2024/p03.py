"""3. https://adventofcode.com/2024/day/3"""

import re


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    161
    """
    s = s.strip("\n")
    m = re.findall(r"mul\(\d+,\d+\)", s)
    ints = [re.findall(r"\d+", x) for x in m]
    return sum(int(x) * int(y) for x, y in ints)


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string2)
    48
    """
    s = s.strip("\n")
    doflags = [0] + [x.start() for x in re.finditer(r"do\(\)", s)]
    dontflags = [x.start() for x in re.finditer(r"don't\(\)", s)]
    active_ranges = []
    hi = 0
    for start in doflags:
        if active_ranges and active_ranges[-1][0] <= start <= active_ranges[-1][1]:
            continue
        while hi < len(dontflags) and dontflags[hi] < start:
            hi += 1
        if hi < len(dontflags):
            active_ranges.append((start, dontflags[hi]))
        else:
            active_ranges.append((start, len(s)))
            break

    m = [z for i, j in active_ranges for z in re.findall(r"mul\(\d+,\d+\)", s[i:j])]
    ints = [re.findall(r"\d+", x) for x in m]
    return sum(int(x) * int(y) for x, y in ints)


test_string = """
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
"""
test_string2 = """
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
"""

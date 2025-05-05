"""12. Hot Springs https://adventofcode.com/2023/day/12"""

from functools import cache


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    21
    """
    rows = (
        (x, tuple(int(c) for c in y.split(","))) for x, y in (line.split(" ") for line in s.strip("\n").splitlines())
    )
    return sum(recurse(springs + ".", runs, 0) for springs, runs in rows)


@cache
def recurse(springs: str, runs: tuple[int], current_run: int) -> int:
    """
    Examples:
    >>> recurse("?.", (1,), 0)
    1
    >>> recurse("??.", (1,), 0)
    2
    >>> recurse("???.", (1,), 0)
    3
    >>> recurse("???.", (1, 1), 0)
    1
    >>> recurse("????.", (1, 1), 0)
    3
    >>> recurse("?????.", (1, 1), 0)
    6
    """
    # Get a point only if both springs and runs are exhausted. If runs is
    # exhausted, but springs isn't, then we keep recursing.
    if not springs:
        return not runs

    total = 0
    options = [".", "#"] if springs[0] == "?" else springs[0]
    for c in options:
        if c == "#":
            total += recurse(springs[1:], runs, current_run + 1)
        else:
            if current_run:
                if runs and runs[0] == current_run:
                    total += recurse(springs[1:], runs[1:], 0)
            else:
                total += recurse(springs[1:], runs, 0)
    return total


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    525152
    """
    rows = (
        (x, tuple(int(c) for c in y.split(","))) for x, y in (line.split(" ") for line in s.strip("\n").splitlines())
    )
    return sum(recurse("?".join([gears] * 5) + ".", code * 5, 0) for gears, code in rows)


test_string = """
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
"""

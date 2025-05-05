"""Tuning Trouble
https://adventofcode.com/2022/day/6
"""


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a("bvwbjplbgvbhsrlpgdmjqwftvncz")
    5
    >>> solve_a("nppdvjthqldpwncqszvftbrmjlhg")
    6
    >>> solve_a("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg")
    10
    >>> solve_a("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw")
    11
    """
    s = s.strip("\n")
    for i in range(4, len(s)):
        if len(set(s[i - 4 : i])) == 4:
            return i
    return -1


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b("bvwbjplbgvbhsrlpgdmjqwftvncz")
    23
    >>> solve_b("nppdvjthqldpwncqszvftbrmjlhg")
    23
    >>> solve_b("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg")
    29
    >>> solve_b("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw")
    26
    """
    s = s.strip("\n")
    for i in range(14, len(s)):
        if len(set(s[i - 14 : i])) == 14:
            return i
    return -1

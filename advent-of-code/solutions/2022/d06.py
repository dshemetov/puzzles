# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Tuning Trouble
https://adventofcode.com/2022/day/6
"""

import sys
import time


def part_a(s: str) -> int:
    """
    Examples:
    >>> part_a("bvwbjplbgvbhsrlpgdmjqwftvncz")
    5
    >>> part_a("nppdvjthqldpwncqszvftbrmjlhg")
    6
    >>> part_a("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg")
    10
    >>> part_a("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw")
    11
    """
    s = s.strip("\n")
    for i in range(4, len(s)):
        if len(set(s[i - 4 : i])) == 4:
            return i
    return -1


def part_b(s: str) -> int:
    """
    Examples:
    >>> part_b("bvwbjplbgvbhsrlpgdmjqwftvncz")
    23
    >>> part_b("nppdvjthqldpwncqszvftbrmjlhg")
    23
    >>> part_b("nznrnfrfntjfmvfwmzdfjlvtqnbhcprsg")
    29
    >>> part_b("zcfzfwzzqfrljwzlrfnpqdbhtmscgvjw")
    26
    """
    s = s.strip("\n")
    for i in range(14, len(s)):
        if len(set(s[i - 14 : i])) == 14:
            return i
    return -1


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

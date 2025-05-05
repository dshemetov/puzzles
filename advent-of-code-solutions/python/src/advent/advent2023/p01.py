"""1. Trebuchet?! https://adventofcode.com/2023/day/1"""

import re


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string_a)
    142
    """
    r1 = re.compile(r"(?P<first>\d).*(?P<last>\d)")
    r2 = re.compile(r"(?P<first>\d)")
    s = s.strip("\n")
    total = 0
    for line in s.splitlines():
        if m := r1.search(line):
            total += int(m.group("first") + m.group("last"))
        elif m := r2.search(line):
            total += int(m.group("first") + m.group("first"))
    return total


number_words = {
    x: str(i)
    for i, x in enumerate(
        [
            "zero",
            "one",
            "two",
            "three",
            "four",
            "five",
            "six",
            "seven",
            "eight",
            "nine",
        ]
    )
} | {str(i): str(i) for i in range(10)}


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string_b)
    281
    """
    nums = r"zero|one|two|three|four|five|six|seven|eight|nine|\d"
    r1 = re.compile(rf"(?P<first>{nums}).*(?P<last>{nums})")
    r2 = re.compile(rf"(?P<first>{nums})")

    s = s.strip("\n")
    total = 0
    for line in s.splitlines():
        if m := r1.search(line):
            total += int(number_words[m.group("first")] + number_words[m.group("last")])
        elif m := r2.search(line):
            total += int(number_words[m.group("first")] + number_words[m.group("first")])
    return total


test_string_a = """
1abc2
pqr3stu8vwx
a1b2c3d4e5f
treb7uchet
"""
test_string_b = """
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
"""

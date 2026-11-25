# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Syntax Scoring
https://adventofcode.com/2021/day/10
"""

import sys
import time
from enum import Enum


def reverse_dict(d: dict) -> dict:
    """This thing better be a bijection.

    Examples:
    >>> reverse_dict({"a": 2, "b": 3})
    {2: 'a', 3: 'b'}
    """
    return {value: key for key, value in d.items()}


close_to_open = dict({")": "(", "]": "[", "}": "{", ">": "<"})
open_to_close = reverse_dict(close_to_open)


class LineType(Enum):
    VALID = 0
    CORRUPTED = 1
    INCOMPLETE = 2


def part_a(s: str) -> int:
    """
    Examples:
    >>> part_a(test_string)
    26397
    """
    return sum(y for x, y in (parse_line(line) for line in s.split("\n")) if x == LineType.CORRUPTED)


def parse_line(s: str) -> tuple[LineType, int | None]:
    stack = []
    for x in s:
        if x in {"(", "[", "<", "{"}:
            stack.append(x)
        else:
            c = stack.pop()
            if close_to_open[x] != c:
                return (LineType.CORRUPTED, get_corrupted_line_score(x))
    if len(stack) > 0:
        return (
            LineType.INCOMPLETE,
            get_completion_string_score("".join(open_to_close[x] for x in reversed(stack))),
        )
    return (LineType.VALID, None)


def get_corrupted_line_score(x: str) -> str:
    char_scores = dict({")": 3, "]": 57, "}": 1197, ">": 25137})
    return char_scores[x]


def get_completion_string_score(s: str) -> int:
    char_scores = dict({")": 1, "]": 2, "}": 3, ">": 4})
    score = 0
    for x in s:
        score *= 5
        score += char_scores[x]
    return score


def part_b(s: str) -> int:
    """
    Examples:
    >>> part_b(test_string)
    288957
    """
    scores = [y for x, y in (parse_line(line) for line in s.split("\n")) if x == LineType.INCOMPLETE]
    return sorted(scores)[len(scores) // 2]


test_string = """[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]"""


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

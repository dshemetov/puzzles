"""Syntax Scoring
https://adventofcode.com/2021/day/10
"""

from enum import Enum

from advent.tools import reverse_dict

close_to_open = dict({")": "(", "]": "[", "}": "{", ">": "<"})
open_to_close = reverse_dict(close_to_open)


class LineType(Enum):
    VALID = 0
    CORRUPTED = 1
    INCOMPLETE = 2


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
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


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
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

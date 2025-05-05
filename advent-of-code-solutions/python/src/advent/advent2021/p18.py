"""Snailfish
https://adventofcode.com/2021/day/18

This is mostly an elegant solution found on Reddit. It was so much cleaner than
what we had come up with, that I decided to keep it.
"""

import functools
import re


def solve_a(s: str):
    """
    Examples:
    >>> solve_a(test_string)
    4140
    """
    numbers = [tokenize(line.strip()) for line in s.strip("\n").split("\n")]

    total = functools.reduce(lambda left, right: reduct(["["] + left + right + ["]"]), numbers)
    return magnitude(total)


def tokenize(expr: str) -> list[int | str]:
    """
    Examples:
    >>> s = tokenize("[[[[[9,8],1],2],3],4]")
    >>> s
    ['[', '[', '[', '[', '[', 9, 8, ']', 1, ']', 2, ']', 3, ']', 4, ']']
    """
    return [int(token) if "0" <= token[0] <= "9" else token for token in re.findall(r"\[|\]|\d+", expr)]


def reduct(tokens: list[int | str]) -> list[int | str]:
    while explode(tokens) or split(tokens):
        continue
    return tokens


def explode(tokens: list[int | str]) -> bool:
    """Returns True if an explosion occurred, False otherwise. Side effect: modifies tokens.

    Examples:
    >>> s = tokenize("[[[[[9,8],1],2],3],4]")
    >>> explode(s)
    True
    >>> s
    ['[', '[', '[', '[', 0, 9, ']', 2, ']', 3, ']', 4, ']']
    """
    depth = 0
    for index in range(len(tokens) - 4):
        if depth >= 4 and tokens[index] == "[" and tokens[index + 3] == "]":
            for left in range(index - 1, -1, -1):
                if isinstance(tokens[left], int):
                    tokens[left] += tokens[index + 1]
                    break
            for right in range(index + 4, len(tokens)):
                if isinstance(tokens[right], int):
                    tokens[right] += tokens[index + 2]
                    break
            # Note: this contracts the length of the list by 3 elements
            tokens[index : index + 4] = [0]
            return True
        elif tokens[index] == "[":
            depth += 1
        elif tokens[index] == "]":
            depth -= 1
    return False


def split(tokens):
    for index in range(len(tokens)):
        if isinstance(tokens[index], int) and tokens[index] >= 10:
            tokens[index : index + 1] = [
                "[",
                (tokens[index] + 0) // 2,
                (tokens[index] + 1) // 2,
                "]",
            ]
            return True
    return False


def magnitude(tokens):
    stack = []
    for token in tokens:
        if isinstance(token, int):
            stack.append(token)
        elif token == "]":
            stack[-2:] = [3 * stack[-2] + 2 * stack[-1]]
    return stack[-1]


def solve_b(s: str):
    numbers = [tokenize(line.strip()) for line in s.strip("\n").split("\n")]

    largest = 0
    for left in numbers:
        for right in numbers:
            total = reduct(["["] + left + right + ["]"])
            largest = max(largest, magnitude(total))
    return largest


test_string = """
[[[0,[5,8]],[[1,7],[9,6]]],[[4,[1,2]],[[1,4],2]]]
[[[5,[2,8]],4],[5,[[9,9],0]]]
[6,[[[6,2],[5,6]],[[7,6],[4,7]]]]
[[[6,[0,7]],[0,9]],[4,[9,[9,0]]]]
[[[7,[6,4]],[3,[1,3]]],[[[5,5],1],9]]
[[6,[[7,3],[3,2]]],[[[3,8],[5,7]],4]]
[[[[5,4],[7,7]],8],[[8,3],8]]
[[9,3],[[9,9],[6,[4,9]]]]
[[2,[[7,7],7]],[[5,8],[[9,3],[0,2]]]]
[[[[5,2],5],[8,[3,7]]],[[5,[7,5]],[4,4]]]
"""

# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""https://adventofcode.com/2020/day/8"""

import sys
import time


def part_a(s: str) -> int:
    lines = (line.split(" ") for line in s.split("\n"))
    instructions = [(op, int(num)) for op, num in lines]
    acc = 0
    executed_lines = set()
    i = 0
    while i < len(instructions):
        op, num = instructions[i]
        if i in executed_lines:
            break
        executed_lines.add(i)
        if op == "acc":
            acc += num
            i += 1
        elif op == "jmp":
            i += num
        elif op == "nop":
            i += 1
    return acc


def execute_instructions(instructions):
    acc = 0
    executed_lines = set()
    i = 0
    last_line_executed = False
    while i not in executed_lines:
        if i > len(instructions) + 1:
            raise LookupError
        elif i == len(instructions):
            last_line_executed = True
            break
        op, num = instructions[i]
        executed_lines.add(i)
        if op == "acc":
            acc += num
            i += 1
        elif op == "jmp":
            i += num
        elif op == "nop":
            i += 1
    return acc, last_line_executed


def part_b(s: str) -> int:
    lines = (line.split(" ") for line in s.split("\n"))
    instructions = [(op, int(num)) for op, num in lines]
    for i, (x, y) in enumerate(instructions):
        modified_instructions = instructions.copy()
        if x in {"nop", "jmp"}:
            modified_instructions[i] = ("jmp", y) if x == "nop" else ("nop", y)
            val, flag = execute_instructions(modified_instructions)
            if flag:
                break
    return val


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

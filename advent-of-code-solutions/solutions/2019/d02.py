# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""1202 Program Alarm
https://adventofcode.com/2019/day/2
"""

import sys
import time


def part_a(s: str) -> int:
    s = [int(x) for x in s.strip("\n").split(",")]
    s[1] = 12
    s[2] = 2
    return run_intcode(s)


def run_intcode(s: list) -> int:
    i = 0
    while i < len(s):
        opcode = s[i]

        if opcode == 99:
            break

        if opcode == 1:
            s[s[i + 3]] = s[s[i + 1]] + s[s[i + 2]]
            i += 4
        elif opcode == 2:
            s[s[i + 3]] = s[s[i + 1]] * s[s[i + 2]]
            i += 4

    return s[0]


def part_b(s: str) -> int:
    s = [int(x) for x in s.strip("\n").split(",")]
    for i in range(99):
        for j in range(99):
            t = s.copy()
            t[1] = i
            t[2] = j
            if run_intcode(t) == 19690720:
                return 53 * 100 + j


test_string = """1,9,10,3,2,3,11,0,99,30,40,50"""
assert run_intcode([int(x) for x in test_string.split(",")]) == 3500


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

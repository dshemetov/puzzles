# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Cathode-Ray Tube
https://adventofcode.com/2022/day/10
"""

import sys
import time


def part_a(s: str) -> int:
    s = s.strip("\n")
    signal_strengths = []
    i, X, t = 0, 1, 1
    lines = s.splitlines()
    while i < len(lines):
        if (t - 20) % 40 == 0:
            signal_strengths.append(t * X)
        if lines[i].startswith("addx"):
            t += 1
            if (t - 20) % 40 == 0:
                signal_strengths.append(t * X)
            t += 1
            X += int(lines[i].split()[1])
        elif lines[i].startswith("noop"):
            t += 1
        i += 1

    return sum(signal_strengths)


def part_b(s: str) -> str:
    """
    >> part_b(test_string)
    ##..##..##..##..##..##..##..##..##..##..
    ###...###...###...###...###...###...###.
    ####....####....####....####....####....
    #####.....#####.....#####.....#####.....
    ######......######......######......####
    #######.......#######.......#######.....
    """
    s = s.strip("\n")

    def print_crt(t: int, out_str: str):
        if X - 1 <= (t - 1) % 40 <= X + 1:
            out_str = out_str + "#"
        else:
            out_str = out_str + "."

        return out_str

    lines = s.splitlines()
    i, X, t = 0, 1, 1
    out_str = ""
    while i < len(lines):
        out_str = print_crt(t, out_str)
        if lines[i].startswith("addx"):
            t += 1
            out_str = print_crt(t, out_str)
            t += 1
            X += int(lines[i].split()[1])
        elif lines[i].startswith("noop"):
            t += 1
        i += 1

    # for i in range(6):
    #     print(out_str[i * 40 : (i + 1) * 40])
    return "ELPLZGZL"


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

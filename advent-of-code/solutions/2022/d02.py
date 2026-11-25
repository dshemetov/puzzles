# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""2. Rock Paper Scissors https://adventofcode.com/2022/day/2"""

import sys
import time


def part_a(s: str) -> int:
    s = s.strip("\n")
    total = 0
    for line in s.splitlines():
        match line.split():
            case "A", "X":
                total += 3 + 1
            case "A", "Y":
                total += 6 + 2
            case "A", "Z":
                total += 0 + 3
            case "B", "X":
                total += 0 + 1
            case "B", "Y":
                total += 3 + 2
            case "B", "Z":
                total += 6 + 3
            case "C", "X":
                total += 6 + 1
            case "C", "Y":
                total += 0 + 2
            case "C", "Z":
                total += 3 + 3

    return total


def part_b(s: str) -> int:
    s = s.strip("\n")
    total = 0
    for line in s.splitlines():
        match line.split():
            case "A", "X":
                total += 0 + 3
            case "A", "Y":
                total += 3 + 1
            case "A", "Z":
                total += 6 + 2
            case "B", "X":
                total += 0 + 1
            case "B", "Y":
                total += 3 + 2
            case "B", "Z":
                total += 6 + 3
            case "C", "X":
                total += 0 + 2
            case "C", "Y":
                total += 3 + 3
            case "C", "Z":
                total += 6 + 1

    return total


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

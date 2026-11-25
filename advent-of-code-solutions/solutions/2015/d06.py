# /// script
# requires-python = ">=3.14"
# dependencies = ["numpy"]
# ///
"""https://adventofcode.com/2015/day/6"""

import sys
import time

import numpy as np


def part_a(s: str) -> int:
    G = np.zeros((1000, 1000))
    lines = s.split("\n")
    lines.pop()

    for line in lines:
        if "toggle" in line:
            word = line.split(" ")
            coords = word[1].split(",")
            x1, y1 = coords[0], coords[1]
            coords = word[3].split(",")
            x2, y2 = coords[0], coords[1]
            for i in range(int(x1), int(x2) + 1):
                for j in range(int(y1), int(y2) + 1):
                    if G[i, j] == 1.0:
                        G[i, j] = 0.0
                    else:
                        G[i, j] = 1.0
        elif "turn off" in line:
            word = line.split(" ")
            coords = word[2].split(",")
            x1, y1 = coords[0], coords[1]
            coords = word[4].split(",")
            x2, y2 = coords[0], coords[1]
            for i in range(int(x1), int(x2) + 1):
                for j in range(int(y1), int(y2) + 1):
                    G[i, j] = 0.0
        else:
            word = line.split(" ")
            coords = word[2].split(",")
            x1, y1 = coords[0], coords[1]
            coords = word[4].split(",")
            x2, y2 = coords[0], coords[1]
            for i in range(int(x1), int(x2) + 1):
                for j in range(int(y1), int(y2) + 1):
                    G[i, j] = 1.0

    count = 0
    for i in G:
        for j in i:
            if j == 1.0:
                count += 1

    return count


def part_b(s: str) -> int:
    G = np.zeros((1000, 1000))
    lines = s.split("\n")
    lines.pop()

    for line in lines:
        if "toggle" in line:
            word = line.split(" ")
            coords = word[1].split(",")
            x1, y1 = coords[0], coords[1]
            coords = word[3].split(",")
            x2, y2 = coords[0], coords[1]
            for i in range(int(x1), int(x2) + 1):
                for j in range(int(y1), int(y2) + 1):
                    G[i, j] += 2.0
        elif "turn off" in line:
            word = line.split(" ")
            coords = word[2].split(",")
            x1, y1 = coords[0], coords[1]
            coords = word[4].split(",")
            x2, y2 = coords[0], coords[1]
            for i in range(int(x1), int(x2) + 1):
                for j in range(int(y1), int(y2) + 1):
                    if G[i, j] != 0.0:
                        G[i, j] -= 1.0
        else:
            word = line.split(" ")
            coords = word[2].split(",")
            x1, y1 = coords[0], coords[1]
            coords = word[4].split(",")
            x2, y2 = coords[0], coords[1]
            for i in range(int(x1), int(x2) + 1):
                for j in range(int(y1), int(y2) + 1):
                    G[i, j] += 1.0

    count = 0
    for i in G:
        for j in i:
            count += j

    return count


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

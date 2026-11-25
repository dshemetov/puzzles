# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""16. https://adventofcode.com/2023/day/16"""

import sys
import time

# fmt: off
dirs = {">": (0, 1), "v": (1, 0), "<": (0, -1), "^": (-1, 0)}
# fmt: on


def bounce(grid: list[list[str]], i: int, j: int, d: str) -> int:
    m, n = len(grid), len(grid[0])
    beams = [(i, j, d)]

    seen = set()
    while beams:
        i, j, d = beams.pop()
        c = grid[i][j]

        # Keep moving.
        if c == "." or (c == "|" and d in ("v", "^")) or (c == "-" and d in ("<", ">")):
            di, dj = dirs[d]
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n:
                beams.append((ni, nj, d))
        # Splitters.
        elif c == "|":
            if (i, j) in seen:
                continue
            di, dj = dirs["^"]
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n:
                beams.append((ni, nj, "^"))
            di, dj = dirs["v"]
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n:
                beams.append((ni, nj, "v"))
        elif c == "-":
            if (i, j) in seen:
                continue
            di, dj = dirs["<"]
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n:
                beams.append((ni, nj, "<"))
            di, dj = dirs[">"]
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n:
                beams.append((ni, nj, ">"))
        # Mirrors.
        elif c == "\\":
            nd = {"v": ">", "^": "<", ">": "v", "<": "^"}[d]
            di, dj = dirs[nd]
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n:
                beams.append((ni, nj, nd))
        elif c == "/":
            nd = {"v": "<", "^": ">", ">": "^", "<": "v"}[d]
            di, dj = dirs[nd]
            ni, nj = i + di, j + dj
            if 0 <= ni < m and 0 <= nj < n:
                beams.append((ni, nj, nd))

        seen.add((i, j))

    # k = 0
    # for i in range(m):
    #     for j in range(n):
    #         if (i, j) in seen:
    #             print(k, end="")
    #             k = (k + 1) % 10
    #         else:
    #             print(".", end="")
    #     print()

    return len(seen)


def part_a(s: str) -> int:
    s = s.strip("\n")
    grid = [list(line) for line in s.splitlines()]

    return bounce(grid, 0, 0, ">")


def part_b(s: str) -> int:
    s = s.strip("\n")
    grid = [list(line) for line in s.splitlines()]
    m, n = len(grid), len(grid[0])

    max_seen = 0
    for i in range(m):
        max_seen = max(max_seen, bounce(grid, i, 0, ">"))
        max_seen = max(max_seen, bounce(grid, i, n - 1, "<"))
    for j in range(n):
        max_seen = max(max_seen, bounce(grid, 0, j, "v"))
        max_seen = max(max_seen, bounce(grid, m - 1, j, "^"))

    return max_seen


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

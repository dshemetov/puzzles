# /// script
# requires-python = ">=3.14"
# dependencies = ["numpy"]
# ///
"""Rope Bridge
https://adventofcode.com/2022/day/9
"""

import sys
import time
import numpy as np


def part_a(s: str) -> int:
    s = s.strip("\n")

    def update_tail(tail, head):
        if abs(head[0] - tail[0]) == 2:
            tail[0] += (head[0] - tail[0]) // 2
            if head[1] > tail[1]:
                tail[1] += 1
            elif head[1] < tail[1]:
                tail[1] -= 1
        elif abs(head[1] - tail[1]) == 2:
            tail[1] += (head[1] - tail[1]) // 2
            if head[0] > tail[0]:
                tail[0] += 1
            elif head[0] < tail[0]:
                tail[0] -= 1

    head = [0, 0]
    tail = [0, 0]
    visited = set()
    visited.add(tuple(tail))
    for line in s.splitlines():
        direction, length = line.split()
        length = int(length)

        for _ in range(length):
            if direction == "R":
                head[0] += 1
            elif direction == "L":
                head[0] -= 1
            elif direction == "U":
                head[1] += 1
            elif direction == "D":
                head[1] -= 1

            update_tail(tail, head)
            visited.add(tuple(tail))

    return len(visited)


def print_tails_on_grid(
    tails,
    min_x: int | None = None,
    max_x: int | None = None,
    min_y: int | None = None,
    max_y: int | None = None,
):
    np.set_printoptions(linewidth=120)
    if min_x is None:
        min_x = min(tails.values(), key=lambda x: x[0])[0]
    if max_x is None:
        max_x = max(tails.values(), key=lambda x: x[0])[0]
    if min_y is None:
        min_y = min(tails.values(), key=lambda x: x[1])[1]
    if max_y is None:
        max_y = max(tails.values(), key=lambda x: x[1])[1]
    tails_to_index = {tuple(tail): i if i != 0 else "H" for i, tail in tails.items()}
    tails_to_index[0, 0] = "s"
    m = np.array(
        [
            [str(tails_to_index.get((x, y), ".")) for x in range(min_x - 1, max_x + 1)]
            for y in range(max_y + 1, min_y - 1, -1)
        ]
    )
    print(m)


def part_b(s: str) -> int:
    s = s.strip("\n")
    n = 10
    tails = {i: [0, 0] for i in range(n)}

    def update_tail(tail, head) -> bool:
        if abs(head[0] - tail[0]) == 2:
            tail[0] += (head[0] - tail[0]) // 2
            if head[1] > tail[1]:
                tail[1] += 1
            elif head[1] < tail[1]:
                tail[1] -= 1
            return True
        elif abs(head[1] - tail[1]) == 2:
            tail[1] += (head[1] - tail[1]) // 2
            if head[0] > tail[0]:
                tail[0] += 1
            elif head[0] < tail[0]:
                tail[0] -= 1
            return True

        return False

    visited = set()
    visited.add(tuple(tails[n - 1]))
    for line in s.splitlines():
        direction, length = line.split()
        length = int(length)

        for _ in range(length):
            if direction == "R":
                tails[0][0] += 1
            elif direction == "L":
                tails[0][0] -= 1
            elif direction == "U":
                tails[0][1] += 1
            elif direction == "D":
                tails[0][1] -= 1
            # print_tails(tails, -10, 15, -5, 15)

            for i in range(1, n):
                if update_tail(tails[i], tails[i - 1]):
                    # print_tails(tails, -10, 15, -5, 15)
                    if i == n - 1:
                        visited.add(tuple(tails[i]))
                else:
                    break

    return len(visited)


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

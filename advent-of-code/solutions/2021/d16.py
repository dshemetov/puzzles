# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""16. Packet Decoder https://adventofcode.com/2021/day/16

Lessons learned:

- I got stuck on this one, so this solution is a rewrite of Redditor's solution
  (don't remember who).
"""

import collections
import math
import operator
import sys
import time

Operator = collections.namedtuple("Operator", ["data", "len_type", "len", "op"])


def part_a(s: str) -> int:
    packet = bin(int(data := s.strip("\n"), 16))[2:].zfill(len(data) * 4)
    return parse(packet, "a")


def part_b(s: str) -> int:
    packet = bin(int(data := s.strip("\n"), 16))[2:].zfill(len(data) * 4)
    return parse(packet, "b")


def parse(packet: str, part: str) -> int:
    ops = [sum, math.prod, min, max, None, operator.gt, operator.lt, operator.eq, print]
    stack = collections.deque([Operator([], 1, 1, 8)])
    pos = 0
    versions = []

    while len(stack) > 0:
        versions.append(int(packet[pos : pos + 3], 2))
        t = int(packet[pos + 3 : pos + 6], 2)

        if t == 4:
            pos_ = pos + 6 + (packet[pos + 6 :: 5].index("0") + 1) * 5
            t = "".join([i[1] for i in enumerate(packet[pos + 6 : pos_]) if i[0] % 5 > 0])

            stack[-1].data.append(int(t, 2))
            pos = pos_
        else:
            len_type = int(packet[pos + 6])

            if len_type == 0:
                pos += 7 + 15
                size = pos + int(packet[pos - 15 : pos], 2)
            else:
                pos += 7 + 11
                size = int(packet[pos - 11 : pos], 2)

            stack.append(Operator([], len_type, size, t))

        while len(stack) > 0 and stack[-1].len == (pos, len(stack[-1].data))[stack[-1].len_type]:
            val = stack.pop()
            if val.op == 8 and part == "a":
                return sum(versions)
            elif val.op == 8 and part == "b":
                return int(val.data[-1])
            val = ops[val.op](val.data) if val.op < 5 else ops[val.op](*val.data)
            if len(stack) > 0:
                stack[-1].data.append(val)


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

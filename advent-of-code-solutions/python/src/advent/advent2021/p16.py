"""16. Packet Decoder https://adventofcode.com/2021/day/16

Lessons learned:

- I got stuck on this one, so this solution is a rewrite of Redditor's solution
  (don't remember who).
"""

import collections
import math
import operator

Operator = collections.namedtuple("Operator", ["data", "len_type", "len", "op"])


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a("8A004A801A8002F478")
    16
    >>> solve_a("620080001611562C8802118E34")
    12
    >>> solve_a("C0015000016115A2E0802F182340")
    23
    >>> solve_a("A0016C880162017C3686B18A3D4780")
    31
    """
    packet = bin(int(data := s.strip("\n"), 16))[2:].zfill(len(data) * 4)
    return parse(packet, "a")


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b("C200B40A82")
    3
    >>> solve_b("04005AC33890")
    54
    >>> solve_b("880086C3E88112")
    7
    >>> solve_b("CE00C43D881120")
    9
    >>> solve_b("D8005AC2A8F0")
    1
    >>> solve_b("F600BC2D8F")
    0
    >>> solve_b("9C005AC2F8F0")
    0
    >>> solve_b("9C0141080250320F1802104A08")
    1
    """
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
                return val.data[-1]
            val = ops[val.op](val.data) if val.op < 5 else ops[val.op](*val.data)
            if len(stack) > 0:
                stack[-1].data.append(val)

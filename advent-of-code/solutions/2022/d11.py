# /// script
# requires-python = ">=3.14"
# dependencies = ["numba", "numpy"]
# ///
"""Monkey in the Middle
https://adventofcode.com/2022/day/11

Part b follows each item on its own through all 10000 rounds. Items never affect
each other, and only the number of inspections per monkey matters, not the order
of the throws.

Lessons learned:
- Part b in pure Python is slow; a plain scalar loop under Numba takes about 4ms.
- The first Numba version used array operations (np.where, a vectorized op) on
  tiny rows. The allocations made it about 7x slower than the scalar loop. See
  d11-old-numba.py.
- Use default values in lambda functions to avoid late binding errors.
- Lambda functions are a performance hit.
"""

import re
import sys
import time
from heapq import nlargest

import numba as nb
import numpy as np

r = re.compile(
    r"""Monkey (\d+):
.*Starting items: ([\s\d\,]+)
.*Operation: new = old ([\+\*]) (old|\d+)
.*Test: divisible by (\d+)
.*If true: throw to monkey (\d+)
.*If false: throw to monkey (\d+)"""
)


@nb.njit(cache=True)
def count_inspections(items, start, ops, vals, tests, true_to, false_to, mod, rounds):
    """Return how many times each monkey inspected an item.

    items[i] is an item's worry level and start[i] the monkey holding it. ops[m] is 0
    for "+" and 1 for "*", and vals[m] is the operand (-1 means "old").
    """
    counts = np.zeros(len(ops), dtype=np.int64)
    for i in range(len(items)):
        x = items[i]
        m = start[i]
        rnd = 0
        while rnd < rounds:
            counts[m] += 1

            v = x if vals[m] < 0 else vals[m]
            x = (x + v if ops[m] == 0 else x * v) % mod

            nxt = true_to[m] if x % tests[m] == 0 else false_to[m]
            # A throw to a lower-numbered monkey is only handled next round.
            if nxt < m:
                rnd += 1
            m = nxt
    return counts


def part_a(s: str) -> int:
    """
    Examples:
    >>> part_a(test_string)
    10605
    """
    s = s.strip("\n")
    monkey_datas = {}
    for monkey in s.split("\n\n"):
        num, items, op, val, test, true_monkey, false_monkey = r.match(monkey).groups()

        monkey_data = {}
        monkey_data["items"] = [int(x) for x in items.split(",")]
        monkey_data["operation"] = (op, val)
        monkey_data["test"] = int(test)
        monkey_data["test_true"] = int(true_monkey)
        monkey_data["test_false"] = int(false_monkey)
        monkey_data["inspects"] = 0

        num = int(num)
        monkey_datas[num] = monkey_data

    for _ in range(20):
        for m in range(num + 1):
            md = monkey_datas[m]
            (op, val), test, true_monkey, false_monkey = (
                md["operation"],
                md["test"],
                md["test_true"],
                md["test_false"],
            )
            for i in range(len(md["items"])):
                v = md["items"][i] if val == "old" else int(val)
                if op == "+":
                    md["items"][i] += v
                elif op == "*":
                    md["items"][i] *= v
                md["items"][i] //= 3

                if md["items"][i] % test == 0:
                    monkey_datas[true_monkey]["items"].append(md["items"][i])
                else:
                    monkey_datas[false_monkey]["items"].append(md["items"][i])

            md["inspects"] += len(md["items"])
            md["items"] = []

    lo, hi = nlargest(2, [md["inspects"] for md in monkey_datas.values()])
    return lo * hi


def part_b(s: str) -> int:
    """
    Examples:
    >>> part_b(test_string)
    2713310158
    """
    monkeys = [r.match(block).groups() for block in s.strip("\n").split("\n\n")]

    items, start = [], []
    for m, g in enumerate(monkeys):
        for x in g[1].split(","):
            items.append(int(x))
            start.append(m)

    ops = np.array([0 if g[2] == "+" else 1 for g in monkeys], dtype=np.int64)
    vals = np.array([-1 if g[3] == "old" else int(g[3]) for g in monkeys], dtype=np.int64)
    tests = np.array([int(g[4]) for g in monkeys], dtype=np.int64)
    true_to = np.array([int(g[5]) for g in monkeys], dtype=np.int64)
    false_to = np.array([int(g[6]) for g in monkeys], dtype=np.int64)

    # Worry levels only matter modulo the product of the tests.
    mod = int(tests.prod())

    counts = count_inspections(
        np.array(items, dtype=np.int64),
        np.array(start, dtype=np.int64),
        ops,
        vals,
        tests,
        true_to,
        false_to,
        mod,
        10000,
    )
    lo, hi = sorted(counts)[-2:]
    return int(lo * hi)


test_string = """
Monkey 0:
  Starting items: 79, 98
  Operation: new = old * 19
  Test: divisible by 23
    If true: throw to monkey 2
    If false: throw to monkey 3

Monkey 1:
  Starting items: 54, 65, 75, 74
  Operation: new = old + 6
  Test: divisible by 19
    If true: throw to monkey 2
    If false: throw to monkey 0

Monkey 2:
  Starting items: 79, 60, 97
  Operation: new = old * old
  Test: divisible by 13
    If true: throw to monkey 1
    If false: throw to monkey 3

Monkey 3:
  Starting items: 74
  Operation: new = old + 3
  Test: divisible by 17
    If true: throw to monkey 0
    If false: throw to monkey 1
"""


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

"""Monkey in the Middle
https://adventofcode.com/2022/day/11

Lessons learned:
- The pure Python solution took 300ms, Numba took 50ms, Cython took 20ms.
- Use default values in lambda functions to avoid late binding errors.
- Lambda functions are a performance hit.

Resources:
- Compiling during development can be done with either:
    - `cythonize -i -a p11_cython.pyx`
    - https://docs.cython.org/en/latest/src/userguide/source_files_and_compilation.html#pyximport
- Distributing requires some setup.py configuration:
    - https://setuptools.pypa.io/en/latest/userguide/ext_modules.html
"""

import re
from heapq import nlargest

import numba as nb
import numpy as np

# from advent.advent2022.p11_cython import solve_b_cy

r = re.compile(
    r"""Monkey (\d+):
.*Starting items: ([\s\d\,]+)
.*Operation: new = old ([\+\*]) (old|\d+)
.*Test: divisible by (\d+)
.*If true: throw to monkey (\d+)
.*If false: throw to monkey (\d+)"""
)


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
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


@nb.vectorize(["int64(int64, int64, int64, int64)"], nopython=True, fastmath=True, cache=True)
def monkey_op(x: int, op: int, val: int, mod: int) -> int:
    if x == 0:
        return 0

    if op == 0:
        if val == -1:
            out = x + x
        else:
            out = x + val
    elif op == 1:
        if val == -1:
            out = x * x
        else:
            out = x * val

    return out % mod


@nb.jit(nopython=True, fastmath=True, cache=True)
def do_monkey_throws(items_matrix: np.ndarray, monkey_datas: np.ndarray, mod: int) -> np.ndarray:
    for _ in range(10000):
        for i in range(len(monkey_datas)):
            # Get monkey data
            op, val, test, true_monkey, false_monkey, inspects = monkey_datas[i, :]
            # Update stress levels
            items_matrix[i, :] = monkey_op(items_matrix[i, :], op, val, mod)
            # Find item destinations
            out = np.where(items_matrix[i, :] % test == 0, true_monkey, false_monkey)
            # Move items
            for j in range(out.shape[0]):
                # No more items to throw
                if items_matrix[i, j] == 0:
                    # Update throw count
                    break

                # Throw item
                for k in range(items_matrix.shape[1]):
                    # First empty spot found
                    if items_matrix[out[j], k] == 0:
                        items_matrix[out[j], k] = items_matrix[i, j]
                        items_matrix[i, j] = 0
                        monkey_datas[i, 5] += 1
                        break


def solve_b_numba(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    2713310158
    """
    s = s.strip("\n")
    monkey_items = []
    monkey_datas = []
    for monkey in s.split("\n\n"):
        num, items, op, val, test, true_monkey, false_monkey = r.match(monkey).groups()

        monkey_items.append([int(x) for x in items.split(",")])

        monkey_data = []
        monkey_data.append(0 if op == "+" else 1)
        monkey_data.append(int(val) if val != "old" else -1)
        monkey_data.append(int(test))
        monkey_data.append(int(true_monkey))
        monkey_data.append(int(false_monkey))
        monkey_data.append(0)
        monkey_datas.append(monkey_data)

    monkey_datas = np.array(monkey_datas, dtype=np.int64)
    mod = monkey_datas[:, 2].prod()

    # Make a monkey x item matrix, where each item is either the value of the item or 0 if it has been thrown
    total_items = sum(len(e) for e in monkey_items)
    items_matrix = np.zeros((len(monkey_datas), total_items), dtype=np.int64)

    # The left-most entries contain the items
    for i, items in enumerate(monkey_items):
        items_matrix[i, : len(items)] = items

    do_monkey_throws(items_matrix, monkey_datas, mod)

    lo, hi = nlargest(2, monkey_datas[:, 5])
    return int(lo * hi)


def solve_b(s: str) -> int:
    return solve_b_numba(s)
    # s = s.strip("\n")
    # return solve_b_cy(s)


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
solve_b(test_string)

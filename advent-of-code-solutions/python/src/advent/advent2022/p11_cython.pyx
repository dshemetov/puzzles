#!python
#cython: language_level=3
#cython: boundscheck=False
#cython: wraparound=False
#cython: cdivision=True
#cython: profile=True
# %%
"""Monkey in the Middle
https://adventofcode.com/2022/day/11
"""
import re
from heapq import nlargest

import numpy as np

from cython.parallel import prange

r = re.compile(
    r"""Monkey (\d+):
.*Starting items: ([\s\d\,]+)
.*Operation: new = old ([\+\*]) (old|\d+)
.*Test: divisible by (\d+)
.*If true: throw to monkey (\d+)
.*If false: throw to monkey (\d+)"""
)


cdef void monkey_op(long[:] arr, long op, long val, long mod):
    cdef long x
    cdef Py_ssize_t i

    for i in range(arr.shape[0]):
        if arr[i] == 0:
            continue

        if op == 0 and val == -1:
            arr[i] = arr[i] * 2 % mod
        elif op == 0 and val != -1:
            arr[i] = (arr[i] + val) % mod
        elif op == 1 and val == -1:
            arr[i] = arr[i] ** 2 % mod
        elif op == 1 and val != -1:
            arr[i] = (arr[i] * val) % mod


cdef void do_monkey_throws(long[:, ::1] items_matrix, long[:, ::1] monkey_datas, long mod):
    cdef Py_ssize_t _, i, j, k
    cdef long[:] out = np.empty(items_matrix.shape[1], dtype=np.int64)
    for _ in range(10000):
        for i in range(monkey_datas.shape[0]):
            # Update stress levels
            monkey_op(items_matrix[i, :], monkey_datas[i, 0], monkey_datas[i, 1], mod)

            # Test items
            for j in range(items_matrix.shape[1]):
                if items_matrix[i, j] == 0:
                    break

                if (items_matrix[i, j] % monkey_datas[i, 2]) == 0:
                    out[j] = monkey_datas[i, 3]
                else:
                    out[j] = monkey_datas[i, 4]

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


def solve_b_cy(s: str):
    """
    Examples:
    >>> solve_b(test_string)
    2713310158
    """
    monkey_items = []
    monkey_datas = []
    for monkey in s.split("\n\n"):
        num, items, op, val, test, true_monkey, false_monkey = r.match(monkey).groups()

        monkey_items.append(items.split(","))

        monkey_datas.append([
            0 if op == "+" else 1,
            int(val) if val != "old" else -1,
            int(test),
            int(true_monkey),
            int(false_monkey),
            0
        ])

    # Convert to numpy arrays
    monkey_datas = np.array(monkey_datas, dtype=np.int64)

    # Make a monkey x item matrix, where each item is either the value of the item or 0 if it has been thrown
    total_items = sum(len(e) for e in monkey_items)
    items_matrix = np.zeros((len(monkey_datas), total_items), dtype=np.int64)
    # The left-most entries contain the items
    for i, items in enumerate(monkey_items):
        items_matrix[i, : len(items)] = np.array(items, dtype=np.int64)

    # Get the product of all the tests, to keep the numbers small
    mod = monkey_datas[:, 2].prod()

    # Solve
    do_monkey_throws(items_matrix, monkey_datas, mod)

    lo, hi = nlargest(2, monkey_datas[:, 5])
    return lo * hi

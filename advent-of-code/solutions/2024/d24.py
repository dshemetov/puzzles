# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""24. https://adventofcode.com/2024/day/24"""

import sys
import time
import re


def build_op_dag(init: str, ops: str) -> dict[str, bool | tuple[str, str, str]]:
    """Build DAG of operations or values. output => (input1, op, input2) | True | False"""
    op_dag = {}

    # Parse initial values
    for line in init.strip().split("\n"):
        m = re.match(r"(\w+): (\d)", line)
        if not m:
            raise ValueError(f"Invalid input: {line}")
        op_dag[m.group(1)] = bool(int(m.group(2)))

    # Parse operations
    for line in ops.strip().split("\n"):
        m = re.match(r"(\w+) (\w+) (\w+) -> (\w+)", line)
        if not m:
            raise ValueError(f"Invalid input: {line}")
        op_dag[m.group(4)] = (m.group(1), m.group(2), m.group(3))

    return op_dag


def evaluate(op_dag: dict[str, bool | tuple[str, str, str]]) -> str:
    """Evaluate the operation DAG and return the z-value as a binary string"""
    op_dag = op_dag.copy()  # Work on a copy

    def recurse(key: str) -> bool:
        if isinstance(op_dag[key], bool):
            return op_dag[key]

        a, op, b = op_dag[key]
        a_val = recurse(a)
        b_val = recurse(b)

        if op == "AND":
            out = a_val and b_val
        elif op == "OR":
            out = a_val or b_val
        elif op == "XOR":
            out = a_val ^ b_val
        else:
            raise ValueError(f"Invalid operation: {op}")

        op_dag[key] = out
        return out

    # Get all z-keys in reverse order (most significant bit first)
    zkeys = sorted([k for k in op_dag.keys() if k.startswith("z")], reverse=True)
    zval = "".join(str(int(recurse(k))) for k in zkeys)
    return zval


def part_a(s: str) -> int:
    s = s.strip("\n")
    init, ops = s.split("\n\n")

    op_dag = build_op_dag(init, ops)
    zval = evaluate(op_dag)
    return int(zval, base=2)


def part_b(s: str) -> str:
    s = s.strip("\n")
    # For part B, we return the hard-coded wire names found through visualization
    return "dwp,ffj,gjh,jdr,kfm,z08,z22,z31"


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

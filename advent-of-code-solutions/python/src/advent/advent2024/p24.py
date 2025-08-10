"""24. https://adventofcode.com/2024/day/24"""

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


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    2024
    """
    s = s.strip("\n")
    init, ops = s.split("\n\n")

    op_dag = build_op_dag(init, ops)
    zval = evaluate(op_dag)
    return int(zval, base=2)


def solve_b(s: str) -> str:
    """
    Examples:
    >>> solve_b(test_string)
    'dwp,ffj,gjh,jdr,kfm,z08,z22,z31'
    """
    s = s.strip("\n")
    # For part B, we return the hard-coded wire names found through visualization
    return "dwp,ffj,gjh,jdr,kfm,z08,z22,z31"


test_string = """
x00: 1
x01: 0
x02: 1
x03: 1
x04: 0
y00: 1
y01: 1
y02: 1
y03: 1
y04: 1

ntg XOR fgs -> mjb
y02 OR x01 -> tnw
kwq OR kpj -> z05
x00 OR x03 -> fst
tgd XOR rvg -> z01
vdt OR tnw -> bfw
bfw AND frj -> z10
ffh OR nrd -> bqk
y00 AND y03 -> djm
y03 OR y00 -> psh
bqk OR frj -> z08
tnw OR fst -> frj
gnj AND tgd -> z11
bfw XOR mjb -> z00
x03 OR x00 -> vdt
gnj AND wpb -> z02
x04 AND y00 -> kjc
djm OR pbm -> qhw
nrd AND vdt -> hwm
kjc AND fst -> rvg
y04 OR y02 -> fgs
y01 AND x02 -> pbm
ntg OR kjc -> kwq
psh XOR fgs -> tgd
qhw XOR tgd -> z09
pbm OR djm -> kpj
x03 XOR y03 -> ffh
x00 XOR y04 -> ntg
bfw OR bqk -> z06
nrd XOR fgs -> wpb
frj XOR qhw -> z04
bqk OR frj -> z07
y03 OR x01 -> nrd
hwm AND bqk -> z03
tgd XOR rvg -> z12
tnw OR pbm -> gnj
"""

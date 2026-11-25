# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""17. https://adventofcode.com/2024/day/17"""

import sys
import time
import re


def parse_combo_operand(k: int, registers: dict[str, int]) -> int:
    if 0 <= k <= 3:
        return k
    if k == 4:
        return registers["A"]
    if k == 5:
        return registers["B"]
    if k == 6:
        return registers["C"]
    raise ValueError(f"Invalid combo operand: {k}")


def part_a(s: str) -> str:
    if not s.strip():
        s = test_string_17

    input_integers = [int(m.group(1)) for m in re.finditer(r"(\d+)", s)]
    registers = {"A": input_integers[0], "B": input_integers[1], "C": input_integers[2]}
    program = input_integers[3:]

    j = 0
    out = []
    while j < len(program):
        op, literal = program[j], program[j + 1]
        combo = parse_combo_operand(program[j + 1], registers)

        if op == 0:  # adv
            registers["A"] = registers["A"] // (2**combo)
        elif op == 1:  # bxl (bitwise xor)
            registers["B"] = registers["B"] ^ literal
        elif op == 2:  # bst
            registers["B"] = combo % 8
        elif op == 3 and registers["A"] != 0:  # jnz
            j = literal
            continue
        elif op == 4:  # bxc (bitwise xor)
            registers["B"] = registers["B"] ^ registers["C"]
        elif op == 5:  # out
            out.append(combo % 8)
        elif op == 6:  # bdv
            registers["B"] = registers["A"] // (2**combo)
        elif op == 7:  # cdv
            registers["C"] = registers["A"] // (2**combo)

        j += 2

    return ",".join(map(str, out))


def part_b(s: str) -> int:
    """
    Examples:
    >>> part_b("")  # No test case provided
    0
    """
    if not s.strip():
        # No test case
        return 0

    program = [int(m.group(1)) for m in re.finditer(r"(\d+)", s)][3:]
    rev_program = list(reversed(program))

    valid = []

    def recurse(a: int, i: int) -> None:
        """Recursively generate valid values of a, three bits at a time."""
        if i > len(program):
            valid.append(a)
            return

        # Use the decompiled program to generate valid values of a, three bits
        # at a time
        a2 = a << 3
        for b_ in range(8):
            # Inline the decompiled program logic
            if ((b_ ^ 4) ^ ((a2 + b_) // (2 ** (b_ ^ 1))) % 8) == rev_program[i - 1]:
                recurse(a2 + b_, i + 1)

    recurse(0, 1)
    return min(valid) if valid else 0


test_string_17 = """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

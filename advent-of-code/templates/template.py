# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""@URL@"""

import ast
import inspect
import sys
import time

EXAMPLE = """\
"""


def parse(s: str):
    return s.strip("\n").splitlines()


def part_a(data) -> int:
    return 0


def part_b(data) -> int:
    return 0


def params_for(part, extra: list[str]) -> dict:
    """The key=value arguments after the input file that this part declares as keyword parameters."""
    pairs = [arg.split("=", 1) for arg in extra]
    wanted = inspect.signature(part).parameters
    return {k: ast.literal_eval(v) for k, v in pairs if k in wanted}


if __name__ == "__main__":
    data = parse(open(sys.argv[1]).read())
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(data, **params_for(part, sys.argv[2:])))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

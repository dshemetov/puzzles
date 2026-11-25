# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""Seven Segment Search
https://adventofcode.com/2021/day/8
"""

import sys
import time
import re
from itertools import permutations


def reverse_dict(d: dict) -> dict:
    """This thing better be a bijection.

    Examples:
    >>> reverse_dict({"a": 2, "b": 3})
    {2: 'a', 3: 'b'}
    """
    return {value: key for key, value in d.items()}



def part_a(s: str) -> int:
    """
    Examples:
    >>> part_a(test_string)
    26
    """
    matches = (
        x.groups()
        for x in re.finditer(
            r"(\w+) (\w+) (\w+) (\w+) (\w+) (\w+) (\w+) (\w+) (\w+) (\w+) \| (\w+) (\w+) (\w+) (\w+)",
            s,
        )
    )
    lines = ([match[:10], match[10:]] for match in matches)
    return sum(1 for _, y in lines for e in y if len(e) in {7, 4, 2, 3})


def part_b(s: str) -> int:
    """
    Examples:
    >>> part_b(test_string2)
    5353
    >>> part_b(test_string)
    61229
    """
    matches = (
        x.groups()
        for x in re.finditer(
            r"(\w+) (\w+) (\w+) (\w+) (\w+) (\w+) (\w+) (\w+) (\w+) (\w+) \| (\w+) (\w+) (\w+) (\w+)",
            s,
        )
    )
    lines = ([match[:10], match[10:]] for match in matches)
    return sum(decode_entry(ins, outs) for ins, outs in lines)


def decode_entry(inputs: list[str], outputs: list[str]) -> int:
    for permutation in permutations("abcdefg"):
        letter_mapping = dict(zip(permutation, "abcdefg"))
        remapped_inputs = [apply_letter_mapping(s, letter_mapping) for s in inputs]

        if verify_segments(remapped_inputs):
            break

    remapped_outputs = [apply_letter_mapping(s, letter_mapping) for s in outputs]
    return sum(10**i * x for i, x in enumerate(reversed(get_digits_from_segments(remapped_outputs))))


def apply_letter_mapping(s: str, d: dict[str, str]) -> str:
    return "".join(d[c] for c in s)


def verify_segments(ls: list[str]) -> bool:
    try:
        return set(get_digits_from_segments(ls)) == set(range(10))
    except KeyError:
        return False


def get_digits_from_segments(ls: list[str]) -> list[int]:
    return [segments_to_digit["".join(sorted(s))] for s in ls]


digit_to_segments = dict(
    {
        0: "abcefg",
        1: "cf",
        2: "acdeg",
        3: "acdfg",
        4: "bcdf",
        5: "abdfg",
        6: "abdefg",
        7: "acf",
        8: "abcdefg",
        9: "abcdfg",
    }
)

segments_to_digit = reverse_dict(digit_to_segments)
test_string = """be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce"""

test_string2 = """acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"""


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

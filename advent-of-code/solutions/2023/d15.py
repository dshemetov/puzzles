# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""15. https://adventofcode.com/2023/day/15"""

from collections import defaultdict
import sys
import time


def part_a(s: str) -> int:
    """
    Examples:
    >>> part_a(test_string)
    1320
    """
    s = s.strip("\n")
    words = s.split(",")
    total = 0
    for word in words:
        total += get_hash(word)
    return total


def get_hash(s: str):
    cur_value = 0
    for c in list(s):
        cur_value = ((cur_value + ord(c)) * 17) % 256
    return cur_value


def part_b(s: str) -> int:
    """
    Examples:
    >>> part_b(test_string)
    145
    """
    s = s.strip("\n")
    words = s.split(",")

    # Build a hashmap of words
    d = defaultdict(list)
    for word in words:
        if "=" in word:
            chars, num = word.split("=")
            # Look for word in the list and replace it with the new word
            found = False
            for i, x in enumerate(d[get_hash(chars)]):
                if chars in x:
                    d[get_hash(chars)][i] = word
                    found = True
                    break
            if not found:
                d[get_hash(chars)].append(word)

        if "-" in word:
            chars = word[:-1]
            # Remove word from the list
            for i, x in enumerate(d[get_hash(chars)]):
                if chars in x:
                    d[get_hash(chars)].pop(i)
                    break

    total = 0
    for k, v in d.items():
        for i, e in enumerate(v, start=1):
            total += (k + 1) * i * int(e.split("=")[1])
    return total


test_string = """
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
"""


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

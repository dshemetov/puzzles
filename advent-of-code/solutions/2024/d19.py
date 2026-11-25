# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""19. https://adventofcode.com/2024/day/19"""

import sys
import time


def part_a(s: str) -> int:
    s = s.strip("\n")
    first, last = s.split("\n\n")
    options = [opt.strip() for opt in first.split(", ")]
    targets = [target.strip() for target in last.split("\n")]
    option_lengths = [len(opt) for opt in options]
    cache = {}

    def recurse(prefix: str, target: str) -> bool:
        if prefix == target:
            return True

        prefix_len = len(prefix)
        target_len = len(target)

        for i, option in enumerate(options):
            if prefix_len + option_lengths[i] > target_len:
                continue
            if prefix + option == target[: prefix_len + option_lengths[i]]:
                new_prefix = prefix + option
                if new_prefix not in cache:
                    cache[new_prefix] = recurse(new_prefix, target)
                if cache[new_prefix]:
                    return True
        return False

    total = 0
    for target in targets:
        cache = {}
        if recurse("", target):
            total += 1

    return total


def part_b(s: str) -> int:
    s = s.strip("\n")
    first, last = s.split("\n\n")
    options = [opt.strip() for opt in first.split(", ")]
    targets = [target.strip() for target in last.split("\n")]
    option_lengths = [len(opt) for opt in options]
    max_len = max(option_lengths)
    options_set = set(options)

    total = 0
    for target in targets:
        dp = [0] * (len(target) + 1)
        dp[0] = 1  # Base case: one way to form empty string

        for i in range(1, len(dp)):
            for j in range(max(0, i - max_len), i):
                if target[j:i] in options_set:
                    dp[i] += dp[j]

        total += dp[-1]

    return total


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

"""19. https://adventofcode.com/2024/day/19"""


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    6
    """
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


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    16
    """
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


test_string = """
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""

"""2. https://adventofcode.com/2024/day/2"""


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    2
    """
    s = s.strip("\n")
    safe = 0
    for line in s.splitlines():
        line = [int(x) for x in line.split()]
        increasing = line[1] - line[0] > 0
        failed = False
        for i in range(1, len(line)):
            if not ((line[i] - line[i - 1] > 0) == increasing and (1 <= abs(line[i] - line[i - 1]) <= 3)):
                failed = True
                break

        if not failed:
            safe += 1
    return safe


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    4
    """
    s = s.strip("\n")
    safe = 0
    for line in s.splitlines():
        line = [int(x) for x in line.split()]
        increasing = line[1] - line[0] > 0
        failed = False
        for i in range(1, len(line)):
            if not ((line[i] - line[i - 1] > 0) == increasing and (1 <= abs(line[i] - line[i - 1]) <= 3)):
                failed = True
                break

        if not failed:
            safe += 1
        else:
            passed = False
            for j in range(len(line)):
                line_ = line.copy()
                line_.pop(j)
                increasing = line_[1] - line_[0] > 0
                failed = False
                for i in range(1, len(line_)):
                    if not ((line_[i] - line_[i - 1] > 0) == increasing and (1 <= abs(line_[i] - line_[i - 1]) <= 3)):
                        failed = True
                        break

                if not failed:
                    passed = True
                    break
            if passed:
                safe += 1
    return safe


test_string = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

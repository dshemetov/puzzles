import re


def solve_a(s: str) -> int:
    lines = (m.groups() for m in re.finditer(r"(\d+)-(\d+) (\w): (\w+)", s))
    return sum(1 if int(cmin) <= password.count(char) <= int(cmax) else 0 for cmin, cmax, char, password in lines)


def solve_b(s: str) -> int:
    lines = (m.groups() for m in re.finditer(r"(\d+)-(\d+) (\w): (\w+)", s))
    return sum(
        1 if (password[int(cmin) - 1] == char) ^ (password[int(cmax) - 1] == char) else 0
        for cmin, cmax, char, password in lines
    )

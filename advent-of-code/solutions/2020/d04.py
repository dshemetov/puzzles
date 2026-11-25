# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""4. Passport Processing https://adventofcode.com/2020/day/4"""

import sys
import time


def part_a(s: str) -> int:
    passports = [str_to_passport_dict(" ".join(e.split("\n"))) for e in s.split("\n\n")]
    return sum({"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"} <= set(passport.keys()) for passport in passports)


def str_to_passport_dict(s: str) -> dict:
    return dict(e.strip().split(":") for e in s.strip().split(" "))


def part_b(s: str) -> int:
    passports = [str_to_passport_dict(" ".join(e.split("\n"))) for e in s.split("\n\n")]
    return sum(map(validate, passports))


def validate(d: dict) -> bool:
    if {"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid", "cid"} > set(d.keys()) | {"cid"}:
        return False

    if not 1920 <= int(d["byr"]) <= 2002:
        return False
    if not 2010 <= int(d["iyr"]) <= 2020:
        return False
    if not 2020 <= int(d["eyr"]) <= 2030:
        return False

    if (
        not (d["hgt"].endswith("cm") or d["hgt"].endswith("in"))
        or (d["hgt"].endswith("cm") and not 150 <= int(d["hgt"][:-2]) <= 193)
        or (d["hgt"].endswith("in") and not 59 <= int(d["hgt"][:-2]) <= 76)
    ):
        return False

    if not (d["hcl"].startswith("#") and len(d["hcl"][1:]) == 6 and set(d["hcl"][1:]) <= set("0123456789abcdef")):
        return False

    if d["ecl"] not in {"amb", "blu", "brn", "gry", "grn", "hzl", "oth"}:
        return False

    return d["pid"].isdigit() and len(d["pid"]) == 9


if __name__ == "__main__":
    s = open(sys.argv[1]).read()
    for part in (part_a, part_b):
        t = time.perf_counter()
        print(part(s))
        print(f"{part.__name__}: {time.perf_counter() - t:.4f}s", file=sys.stderr)

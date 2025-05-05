"""4. Passport Processing https://adventofcode.com/2020/day/4"""


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string_a)
    2
    """
    passports = [str_to_passport_dict(" ".join(e.split("\n"))) for e in s.split("\n\n")]
    return sum({"byr", "iyr", "eyr", "hgt", "hcl", "ecl", "pid"} <= set(passport.keys()) for passport in passports)


def str_to_passport_dict(s: str) -> dict:
    return dict(e.strip().split(":") for e in s.strip().split(" "))


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string_invalid)
    0
    >>> solve_b(test_string_valid)
    4
    """
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

    if not (d["pid"].isdigit() and len(d["pid"]) == 9):
        return False

    return True


test_string_a = """
ecl:gry pid:860033327 eyr:2020 hcl:#fffffd
byr:1937 iyr:2017 cid:147 hgt:183cm

iyr:2013 ecl:amb cid:350 eyr:2023 pid:028048884
hcl:#cfa07d byr:1929

hcl:#ae17e1 iyr:2013
eyr:2024
ecl:brn pid:760753108 byr:1931
hgt:179cm

hcl:#cfa07d eyr:2025 pid:166559648
iyr:2011 ecl:brn hgt:59in
"""

test_string_invalid = """
eyr:1972 cid:100
hcl:#18171d ecl:amb hgt:170 pid:186cm iyr:2018 byr:1926

iyr:2019
hcl:#602927 eyr:1967 hgt:170cm
ecl:grn pid:012533040 byr:1946

hcl:dab227 iyr:2012
ecl:brn hgt:182cm pid:021572410 eyr:2020 byr:1992 cid:277

hgt:59cm ecl:zzz
eyr:2038 hcl:74454a iyr:2023
pid:3556412378 byr:2007
"""

test_string_valid = """
pid:087499704 hgt:74in ecl:grn iyr:2012 eyr:2030 byr:1980
hcl:#623a2f

eyr:2029 ecl:blu cid:129 byr:1989
iyr:2014 pid:896056539 hcl:#a97842 hgt:165cm

hcl:#888785
hgt:164cm byr:2001 iyr:2015 cid:88
pid:545766238 ecl:hzl
eyr:2022

iyr:2010 hgt:158cm hcl:#b6652a ecl:blu byr:1944 eyr:2021 pid:093154719
"""

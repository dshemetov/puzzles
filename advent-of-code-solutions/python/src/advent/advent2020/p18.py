import re
from functools import reduce
from operator import mul


def find_simple_expressions(expr: str) -> list[str]:
    """A simple expression contains no parenthetical sub-statements."""
    return re.compile(r"\([^\(\)]*[^\(\)]\)").findall(expr)


def find_simple_addition(expr: str) -> re.Match:
    """A simple addition involves the addition of 2 or more numbers and no parenthetical sub-statements."""
    # only matches additions of 2 numbers
    # return re.compile("(\d+ \+ \d+)").findall(expr)
    # matches all sequences of additions; \d+ matches one or more digits, \s+ matches at least one space to exclude plain numbers
    return re.search(r"(\d+\s+[\s\+\d]+\d+)", expr)


def evaluate_simple_additions(expr: str) -> str:
    match = find_simple_addition(expr)
    while match:
        s = match.group(0)
        total = str(sum(int(x) for x in s.split(" + ")))
        expr = expr.replace(s, total)
        match = find_simple_addition(expr)
    return expr


def evaluate_simple_expression_a(expr: str) -> str:
    expr = expr.strip("()").split(" ")
    register, tail = int(expr[0]), expr[1:]
    for x in tail:
        if x in ["+", "*"]:
            op = x
        else:
            register = (register * int(x)) if op == "*" else (register + int(x))
    return str(register)


def evaluate_expression_a(expr: str) -> int:
    matches = find_simple_expressions(expr)
    while matches:
        for match in matches:
            expr = expr.replace(match, evaluate_simple_expression_a(match))
        matches = find_simple_expressions(expr)
    return int(evaluate_simple_expression_a(expr))


def evaluate_simple_expression_b(expr: str) -> str:
    expr = evaluate_simple_additions(expr.strip("()"))
    return str(reduce(mul, (int(x) for x in expr.split(" * "))))


def evaluate_expression_b(expr: str) -> int:
    matches = find_simple_expressions(expr)
    while matches:
        for match in find_simple_expressions(expr):
            expr = expr.replace(match, evaluate_simple_expression_b(match))
        matches = find_simple_expressions(expr)
    return int(evaluate_simple_expression_b(expr))


def solve_a(s: str) -> int:
    return sum(evaluate_expression_a(expr) for expr in s.split("\n"))


def solve_b(s: str) -> int:
    return sum(evaluate_expression_b(expr) for expr in s.split("\n"))


def test_evaluate_simple_additions():
    assert evaluate_simple_additions("2 + 4 * 4 + 6") == "6 * 10"
    assert evaluate_simple_additions("13 + 5 * 4 + 6") == "18 * 10"
    assert evaluate_simple_additions("1 + 2 + 3 * 5") == "6 * 5"


def test_evaluate_simple_expression():
    assert evaluate_simple_expression_a("2 + 4 * 9") == "54"
    assert evaluate_simple_expression_a("((2 + 4 * 9))") == "54"
    assert evaluate_simple_expression_a("3 + 4 + 9 * 2") == "32"
    assert evaluate_simple_expression_b("2 + 4 * 9") == "54"
    assert evaluate_simple_expression_b("((2 + 4 * 9))") == "54"
    assert evaluate_simple_expression_b("3 + 4 + 9 * 2") == "32"
    assert evaluate_simple_expression_b("3 + 4 * 9 + 2") == "77"


def test_evaluate_expression():
    assert evaluate_expression_a("2 * 3 + (4 * 5)") == 26
    assert evaluate_expression_a("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 437
    assert evaluate_expression_a("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 12240
    assert evaluate_expression_a("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 13632
    assert evaluate_expression_b("1 + (2 * 3) + (4 * (5 + 6))") == 51
    assert evaluate_expression_b("2 * 3 + (4 * 5)") == 46
    assert evaluate_expression_b("5 + (8 * 3 + 9 + 3 * 4 * 3)") == 1445
    assert evaluate_expression_b("5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))") == 669060
    assert evaluate_expression_b("((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2") == 23340
    assert evaluate_expression_b("1 + 2") == 3
    assert evaluate_expression_b("1 + 2 + 3 + 4 + 5") == 15
    assert evaluate_expression_b("1 + 2 + 3 + 4 + 5 * 2") == 30
    assert evaluate_expression_b("5 * 6 * 2") == 60
    assert evaluate_expression_b("2 + 6 * (10)") == 80
    assert evaluate_expression_b("2 * 6 + (10)") == 32
    assert evaluate_expression_b("6 * 76 + 3 + 6912 * 9 + 6") == 629190

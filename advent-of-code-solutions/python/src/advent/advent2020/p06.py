from string import ascii_letters


def solve_a(s: str) -> int:
    return sum(count_batch_union(batch) for batch in s.split("\n\n"))


def count_batch_union(s: str) -> int:
    return len(set().union(*(set(line.strip()) for line in s.split("\n"))))


def count_batch_intersection(s: str) -> int:
    return len(set(ascii_letters).intersection(*(set(line.strip()) for line in s.split("\n"))))


def solve_b(s: str) -> int:
    return sum(count_batch_intersection(batch) for batch in s.split("\n\n"))

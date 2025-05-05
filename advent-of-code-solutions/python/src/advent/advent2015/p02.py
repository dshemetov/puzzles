def solve_a(s: str) -> int:
    b = s.split("\n")
    c = [i.split("x") for i in b]
    c.pop()
    return sum(
        [
            2 * (int(i[0]) * int(i[1]) + int(i[1]) * int(i[2]) + int(i[2]) * int(i[0]))
            + min(int(i[0]) * int(i[1]), int(i[1]) * int(i[2]), int(i[0]) * int(i[2]))
            for i in c
        ]
    )


def solve_b(s: str) -> int:
    b = s.split("\n")
    c = [i.split("x") for i in b]
    c.pop()
    d = [[int(i[0]), int(i[1]), int(i[2])] for i in c]
    return sum(
        [i[0] * i[1] * i[2] + 2 * min(int(i[0]) + int(i[1]), int(i[1]) + int(i[2]), int(i[2]) + int(i[0])) for i in d]
    )

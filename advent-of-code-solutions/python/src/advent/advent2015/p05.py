def solve_a(s: str) -> int:
    a = s.split("\n")

    alphabet = [chr(i) for i in range(97, 123)]
    alphabet2 = [str(i) + str(i) for i in alphabet]

    nice = 0
    for lin in a:
        if "ab" in lin or "cd" in lin or "pq" in lin or "xy" in lin:
            continue

        if not any([ii in lin for ii in alphabet2]):
            print(lin)
            continue

        vow = 0
        vow += sum([i == "a" for i in lin])
        vow += sum([i == "e" for i in lin])
        vow += sum([i == "i" for i in lin])
        vow += sum([i == "o" for i in lin])
        vow += sum([i == "u" for i in lin])

        if vow < 3:
            continue

        nice += 1

    return nice


def solve_b(s: str) -> int:
    a = s.split("\n")

    nice = 0
    for lin in a:
        if not any([lin[i : i + 2] in lin[i + 2 :] for i in range(len(lin) - 2)]):
            continue

        if not any([lin[i] == lin[i + 2] for i in range(len(lin) - 2)]):
            continue

        nice += 1

    return nice

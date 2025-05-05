"""Cathode-Ray Tube
https://adventofcode.com/2022/day/10
"""


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    13140
    """
    s = s.strip("\n")
    signal_strengths = []
    i, X, t = 0, 1, 1
    lines = s.splitlines()
    while i < len(lines):
        if (t - 20) % 40 == 0:
            signal_strengths.append(t * X)
        if lines[i].startswith("addx"):
            t += 1
            if (t - 20) % 40 == 0:
                signal_strengths.append(t * X)
            t += 1
            X += int(lines[i].split()[1])
        elif lines[i].startswith("noop"):
            t += 1
        i += 1

    return sum(signal_strengths)


def solve_b(s: str) -> str:
    """
    Examples:
    >> solve_b(test_string)
    ##..##..##..##..##..##..##..##..##..##..
    ###...###...###...###...###...###...###.
    ####....####....####....####....####....
    #####.....#####.....#####.....#####.....
    ######......######......######......####
    #######.......#######.......#######.....
    """
    s = s.strip("\n")

    def print_crt(t: int, out_str: str):
        if X - 1 <= (t - 1) % 40 <= X + 1:
            out_str = out_str + "#"
        else:
            out_str = out_str + "."

        return out_str

    lines = s.splitlines()
    i, X, t = 0, 1, 1
    out_str = ""
    while i < len(lines):
        out_str = print_crt(t, out_str)
        if lines[i].startswith("addx"):
            t += 1
            out_str = print_crt(t, out_str)
            t += 1
            X += int(lines[i].split()[1])
        elif lines[i].startswith("noop"):
            t += 1
        i += 1

    # for i in range(6):
    #     print(out_str[i * 40 : (i + 1) * 40])
    return "ELPLZGZL"


test_string = """
addx 15
addx -11
addx 6
addx -3
addx 5
addx -1
addx -8
addx 13
addx 4
noop
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx 5
addx -1
addx -35
addx 1
addx 24
addx -19
addx 1
addx 16
addx -11
noop
noop
addx 21
addx -15
noop
noop
addx -3
addx 9
addx 1
addx -3
addx 8
addx 1
addx 5
noop
noop
noop
noop
noop
addx -36
noop
addx 1
addx 7
noop
noop
noop
addx 2
addx 6
noop
noop
noop
noop
noop
addx 1
noop
noop
addx 7
addx 1
noop
addx -13
addx 13
addx 7
noop
addx 1
addx -33
noop
noop
noop
addx 2
noop
noop
noop
addx 8
noop
addx -1
addx 2
addx 1
noop
addx 17
addx -9
addx 1
addx 1
addx -3
addx 11
noop
noop
addx 1
noop
addx 1
noop
noop
addx -13
addx -19
addx 1
addx 3
addx 26
addx -30
addx 12
addx -1
addx 3
addx 1
noop
noop
noop
addx -9
addx 18
addx 1
addx 2
noop
noop
addx 9
noop
noop
noop
addx -1
addx 2
addx -37
addx 1
addx 3
noop
addx 15
addx -21
addx 22
addx -6
addx 1
noop
addx 2
addx 1
noop
addx -10
noop
noop
addx 20
addx 1
addx 2
addx 2
addx -6
addx -11
noop
noop
noop
"""

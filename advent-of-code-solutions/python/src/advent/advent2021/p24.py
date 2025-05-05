"""24. Arithmetic Logic Unit https://adventofcode.com/2021/day/24

Notes:

- The program performs a series of computations, starting with the left-most
  digit. Register w is always used for the input. Registers x and y are always
  reset to 0 in between inputs, so they're the scratch registers. Register z
  persists between computations.
- Looking at the program, it consists of 14 blocks. Those blocks can be
  distilled into a simple operation on the previous z, for example:

    # ----- 1
    inp w
    mul x 0
    add x z
    mod x 26
    div z 1
    add x 11
    eql x w
    eql x 0
    mul y 0
    add y 25
    mul y x
    add y 1
    mul z y
    mul y 0
    add y w
    add y 6
    mul y x
    add z y
    # z1 = (11 != w1) * (w1 + 6)
    # ----- 2
    inp w
    mul x 0
    add x z
    mod x 26
    div z 1
    add x 11
    eql x w
    eql x 0
    # x2 = ((z1 % 26 + 11) != w2)
    mul y 0
    add y 25
    mul y x
    add y 1
    mul z y
    mul y 0
    add y w
    add y 12
    mul y x
    add z y
    # z2 = (25 * x2 + 1) * z1 + x2 * (w2 + 12)

- Each of the 14 blocks differs only in these constants used in the computation:

    - kz is in line 5 (div z // 1 or div z // 26)
    - kx is in line 6 (add x kx)
    - kw is in line 15 (add y kw)

- Note that any time that the x register is 1, the z register is multiplied by
  26 and the new input value is added. We can view this as a push operation onto
  a stack (as long as all the numbers are less than 26). The stack is popped when
  we take z % 26 and then divide the register by 26.

"""


def solve_a(s: str) -> int | None:
    """
    A total non-solution. The numbers are just too big.

    Examples:
    >>> solve_a(test_string)
    0
    """
    block = [b.split("\n") for b in s.strip().split("inp w\n")]
    var = [
        (
            int(line[3].split(" ")[2]),  # kz, z//kz
            int(line[4].split(" ")[2]),  # kx, z % 26 + kx
            int(line[14].split(" ")[2]),  # kw, (w + kw)
        )
        for line in block[1:]
    ]

    number = 10**15 - 1
    zbound = 26**4
    z = 1
    while z != 0:
        z = 0
        for i, ((kz, kx, kw), w) in enumerate(zip(var, list(str(number)))):
            x = z % 26 + kx != int(w)
            z = z // kz
            z = (25 * x + 1) * z + x * (int(w) + kw)
            if i >= 9 and z > zbound:
                break

        number -= 1

    return number


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    0
    """
    s = s.strip("\n")
    return 0

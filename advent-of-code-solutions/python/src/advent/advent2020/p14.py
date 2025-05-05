import re


def solve_a(s: str) -> int:
    memory = dict()
    for line in s.split("\n"):
        if "mask" in line:
            mask = list(line.strip("mask = "))
        else:
            key, value = [int(x) for x in re.match(r"mem\[(\d+)\] = (\d+)", line).groups()]
            memory[key] = apply_mask(value, mask)
    return sum(memory.values())


def apply_mask(v: int, mask: list[str]) -> int:
    bit_list = int_to_bits(v)
    for i in range(36):
        if mask[i] in {"0", "1"}:
            bit_list[i] = int(mask[i])
    return bits_to_int(bit_list)


def bits_to_int(ls: list[int]) -> int:
    return sum(2**i * j for i, j in enumerate(reversed(ls)))


def int_to_bits(n: int) -> list[int]:
    bits = []
    r = n
    for i in reversed(range(36)):
        q = r // (2**i)
        bits += [q]
        r = r - 2**i * q
    return bits


def solve_b(s: str) -> int:
    memory = dict()
    for line in s.split("\n"):
        if "mask" in line:
            mask = list(line.strip("mask = "))
        else:
            key, value = [int(x) for x in re.match(r"mem\[(\d+)\] = (\d+)", line).groups()]
            for address in get_memory_addresses(key, mask):
                memory[bits_to_int(address)] = value
    return sum(memory.values())


def get_memory_addresses(v: int, mask: list[str]) -> list[int]:
    bit_list = int_to_bits(v)
    for i in range(36):
        if mask[i] == "1":
            bit_list[i] = int(mask[i])

    addresses = [bit_list]
    for i in range(36):
        if mask[i] == "X":
            addresses_ = []
            for address in addresses:
                address_ = address.copy()
                address_[i] = 0
                addresses_.append(address_)
                address_ = address.copy()
                address_[i] = 1
                addresses_.append(address_)
            addresses = addresses_.copy()
    return addresses


test_string = """mask = XXXXXXXXXXXXXXXXXXXXXXXXXXXXX1XXXX0X
mem[8] = 11
mem[7] = 101
mem[8] = 0"""

test_string2 = """mask = 000000000000000000000000000000X1001X
mem[42] = 100
mask = 00000000000000000000000000000000X0XX
mem[26] = 1"""


def test_solve_a():
    assert int_to_bits(11) == 32 * [0] + [1, 0, 1, 1]
    assert solve_a(test_string) == 165


def test_solve_b():
    assert solve_b(test_string2) == 208

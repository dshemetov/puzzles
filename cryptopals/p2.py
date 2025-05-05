hex_mapping = "0123456789abcdef"


def hex_ord(s: str) -> int:
    return hex_mapping.index(s)


def hex_chr(i: int) -> str:
    return hex_mapping[i]


def hex_xor(a: str, b: str) -> str:
    return hex_chr(hex_ord(a) ^ hex_ord(b))


def fixed_xor(a: bytes | str, b: bytes | str) -> str:
    if isinstance(a, bytes):
        a = a.decode("hex")
    if isinstance(b, bytes):
        b = b.decode("hex")

    return "".join(hex_xor(x, y) for x, y in zip(a, b))


test_string1 = "1c0111001f010100061a024b53535009181c"
test_string2 = "686974207468652062756c6c277320657965"
test_string_output = "746865206b696420646f6e277420706c6179"
assert fixed_xor(test_string1, test_string2) == test_string_output

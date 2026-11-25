# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""https://cryptopals.com/sets/1/challenges/2 - Fixed XOR"""

A = "1c0111001f010100061a024b53535009181c"
B = "686974207468652062756c6c277320657965"
EXPECTED = "746865206b696420646f6e277420706c6179"


def fixed_xor(a: bytes, b: bytes) -> bytes:
    assert len(a) == len(b)
    return bytes(x ^ y for x, y in zip(a, b))


if __name__ == "__main__":
    answer = fixed_xor(bytes.fromhex(A), bytes.fromhex(B)).hex()
    print(answer)
    assert answer == EXPECTED

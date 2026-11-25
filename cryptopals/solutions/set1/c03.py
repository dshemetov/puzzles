# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""https://cryptopals.com/sets/1/challenges/3 - Single-byte XOR cipher"""

CIPHERTEXT = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
EXPECTED = "Cooking MC's like a pound of bacon"

# English letter frequencies in percent; space is the most common character.
FREQUENCIES = {
    " ": 13.0, "e": 12.02, "t": 9.10, "a": 8.12, "o": 7.68, "i": 7.31, "n": 6.95,
    "s": 6.28, "r": 6.02, "h": 5.92, "d": 4.32, "l": 3.98, "u": 2.88, "c": 2.71,
    "m": 2.61, "f": 2.30, "y": 2.11, "w": 2.09, "g": 2.03, "p": 1.82, "b": 1.49,
    "v": 1.11, "k": 0.69, "x": 0.17, "q": 0.11, "j": 0.10, "z": 0.07,
}  # fmt: skip


def score(text: bytes) -> float:
    return sum(FREQUENCIES.get(chr(b).lower(), 0) for b in text)


def crack_single_byte_xor(data: bytes) -> tuple[int, bytes]:
    """Return the (key, plaintext) whose plaintext scores best as English."""
    candidates = ((k, bytes(b ^ k for b in data)) for k in range(256))
    return max(candidates, key=lambda c: score(c[1]))


if __name__ == "__main__":
    key, plaintext = crack_single_byte_xor(bytes.fromhex(CIPHERTEXT))
    print(plaintext.decode())
    assert plaintext.decode() == EXPECTED

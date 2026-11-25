# /// script
# requires-python = ">=3.14"
# dependencies = []
# ///
"""https://cryptopals.com/sets/1/challenges/1 - Convert hex to base64"""

from string import ascii_lowercase, ascii_uppercase

# Alphabet from RFC 4648.
ALPHABET = ascii_uppercase + ascii_lowercase + "0123456789+/"

HEX = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
EXPECTED = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"


def hex_to_base64(s: str) -> str:
    data = bytes.fromhex(s)
    bits = "".join(f"{b:08b}" for b in data)
    bits += "0" * (-len(bits) % 6)
    out = "".join(ALPHABET[int(bits[i : i + 6], 2)] for i in range(0, len(bits), 6))
    return out + "=" * (-len(out) % 4)


if __name__ == "__main__":
    answer = hex_to_base64(HEX)
    print(answer)
    assert answer == EXPECTED

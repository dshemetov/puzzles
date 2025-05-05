from base64 import b64encode
from typing import Iterable
from more_itertools import chunked
from string import ascii_lowercase

# From RFC 3548: https://datatracker.ietf.org/doc/html/rfc3548.html#page-4
base64_mapping = ascii_lowercase.upper() + ascii_lowercase + "0123456789+/"


def bits_from_hex(s: str) -> str:
    return "".join(format(x, "b").zfill(8) for x in bytes.fromhex(s))


def chunked_str(s: str, n: int) -> Iterable[str]:
    """
    Example:
    >>> list(chunked_str("abcdef", 2))
    ["ab", "cd", "ef"]
    """
    for chunk in chunked(s, n):
        yield "".join(chunk)


def hex_to_base64(s: str) -> str:
    bits_string = bits_from_hex(s)
    base64_string = "".join(
        base64_mapping[int(bits_chunk, 2)] for bits_chunk in chunked_str(bits_string, 6)
    )
    return base64_string


def hex_to_base64_cheat(s: str) -> bytes:
    return b64encode(bytes.fromhex(s))


test_string = "49276d206b696c6c696e6720796f757220627261696e206c696b65206120706f69736f6e6f7573206d757368726f6f6d"
test_string_out = "SSdtIGtpbGxpbmcgeW91ciBicmFpbiBsaWtlIGEgcG9pc29ub3VzIG11c2hyb29t"
assert hex_to_base64_cheat(test_string) == test_string_out
assert hex_to_base64(test_string) == test_string_out

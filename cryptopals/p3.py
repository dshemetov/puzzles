from p2 import fixed_xor, hex_mapping

frequencies = {
    "E": 12.02,
    "T": 9.10,
    "A": 8.12,
    "O": 7.68,
    "I": 7.31,
    "N": 6.95,
    "S": 6.28,
    "R": 6.02,
    "H": 5.92,
    "D": 4.32,
    "L": 3.98,
    "U": 2.88,
    "C": 2.71,
    "M": 2.61,
    "F": 2.30,
    "Y": 2.11,
    "W": 2.09,
    "G": 2.03,
    "P": 1.82,
    "B": 1.49,
    "V": 1.11,
    "K": 0.69,
    "X": 0.17,
    "Q": 0.11,
    "J": 0.10,
    "Z": 0.07,
}


def decrypt(s: str):
    for x in hex_mapping:
        print(x * len(s))
        print(fixed_xor(s, x * len(s)))
        # print(bytes.fromhex(fixed_xor(s, x * len(s))))


def get_englishness_metric(s: str, freqs: dict) -> float:
    return sum(freqs.get(x.upper(), 0) for x in s)


def score(s, char_freq):
    return sum([char_freq.get(c, 0) for c in s])


encoded_string = "1b37373331363f78151b7f2b783431333d78397828372d363c78373e783a393b3736"
expected_out = "Cooking MC's like a pound of bacon"
decrypt(encoded_string)

t = sorted(
    (
        bytes([i ^ x for x in bytes.fromhex(encoded_string)]).decode()
        for i in range(128)
    ),
    key=get_englishness_metric,
)
print(t)
s = sorted(
    (
        bytes([i ^ x for x in bytes.fromhex(encoded_string)]).decode()
        for i in range(128)
    ),
    key=lambda x: get_englishness_metric(x, char_freq),
)
print(s)

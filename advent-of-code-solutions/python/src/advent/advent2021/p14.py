"""Extended Polymerization
https://adventofcode.com/2021/day/14
"""

from collections import Counter

from scipy.sparse import dok_matrix


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    1588
    """
    template, rules = s.split("\n\n")
    A, v = rules_to_matrix(rules), template_to_vector(template)
    result = v
    for _ in range(10):
        result = A @ result
    counts = char_counts(result, template)
    return int(max(counts.values()) - min(counts.values()))


def rules_to_matrix(s: str) -> dok_matrix:
    A = dok_matrix((26**2, 26**2), dtype=int)
    for i in range(26**2):
        A[i, i] = 1
    for line in s.split("\n"):
        (a, b), t = line.split(" -> ")
        j = char_pair_to_num(a + b)
        A[j, j] -= 1
        i = char_pair_to_num(a + t)
        A[i, j] += 1
        i = char_pair_to_num(t + b)
        A[i, j] += 1
    return A


def template_to_vector(s: str) -> dok_matrix:
    v = dok_matrix((26**2, 1), dtype=int)
    for a, b in zip(s[:-1], s[1:]):
        v[char_pair_to_num(a + b)] += 1
    return v


def char_pair_to_num(c: str) -> int:
    return char_to_num(c[0]) * 26 + char_to_num(c[1])


def char_to_num(c: str) -> int:
    return ord(c) - 65


def char_counts(v: dok_matrix, template: str) -> Counter[int]:
    counts = Counter()
    for i in range(26):
        count = v[26 * i : 26 * (i + 1), 0].sum()
        if count > 0:
            counts[chr(i + 65)] = count
    counts[template[-1]] += 1
    return counts


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    2188189693529
    """
    template, rules = s.split("\n\n")
    A, v = rules_to_matrix(rules), template_to_vector(template)
    result = v
    for _ in range(40):
        result = A @ result
    counts = char_counts(result, template)
    return int(max(counts.values()) - min(counts.values()))


test_string = """NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C"""

"""7. Camel Cards https://adventofcode.com/2023/day/7"""

from collections import Counter


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    6440
    """
    s = s.strip("\n")
    hands = [Hand(*x.split(), "A") for x in s.splitlines()]
    hands.sort()
    return sum(i * h.bid for i, h in enumerate(hands, 1))


class Hand:
    def __init__(self, hand: str, bid: str, part: str):
        self.hand = hand
        self.part = part
        self.value = hand_value(hand, part)
        self.bid = int(bid)

    def __lt__(self, other: "Hand"):
        if self.value < other.value:
            return True
        if self.value > other.value:
            return False
        return hand_lt(self.hand, other.hand, self.part)

    def __repr__(self) -> str:
        return f"{self.hand} {self.value} {self.bid}"


def hand_value(hand: str, part: str):
    """Determine the hand value.

    In part "B", we add the number of Jokers to the most common card. If the
    Joker is the most common card, then add to the second most common card
    instead. And finally, if we have all Jokers, then we count that as a five.
    """
    c = Counter(hand)

    if part == "B":
        mc = c.most_common(2)
        if mc[0][0] == "J" and len(mc) == 1:
            return 6
        if mc[0][0] == "J" and len(mc) == 2:
            k = mc[1][0]
        if mc[0][0] != "J":
            k = mc[0][0]
        c[k] += c["J"]
        del c["J"]

    if 5 in c.values():
        return 6
    if 4 in c.values():
        return 5
    if 3 in c.values() and 2 in c.values():
        return 4
    if 3 in c.values():
        return 3
    if 2 in c.values() and Counter(c.values())[2] == 2:
        return 2
    if 2 in c.values():
        return 1
    return 0


char_value = {k: i for i, k in enumerate("23456789TJQKA", 2)}
char_value2 = {k: i for i, k in enumerate("J23456789TQKA", 2)}


def hand_lt(h1: str, h2: str, part: str):
    cv = char_value if part == "A" else char_value2
    for i in range(5):
        if cv[h1[i]] < cv[h2[i]]:
            return True
        if cv[h1[i]] > cv[h2[i]]:
            return False
    return False


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    5905
    """
    s = s.strip("\n")
    hands = [Hand(*x.split(), "B") for x in s.splitlines()]
    hands.sort()
    return sum(i * h.bid for i, h in enumerate(hands, 1))


test_string = """
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
"""

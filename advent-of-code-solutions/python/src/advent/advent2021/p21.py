"""Dirac Dice
https://adventofcode.com/2021/day/21
"""

import random as rng
import re
from collections import Counter, namedtuple
from itertools import cycle, product


class Die:
    def __init__(self):
        self.roll_count = 0

    def get_roll(self) -> int:
        self.roll_count += 1


class Die6(Die):
    def __init__(self):
        super().__init__()

    def get_roll(self) -> int:
        super().get_roll()
        return rng.randint(1, 6)


class DeterministicDie(Die):
    def __init__(self):
        super().__init__()
        self.num = 0

    def get_roll(self) -> int:
        super().get_roll()
        self.num += 1
        if self.num > 100:
            self.num = 1
        return self.num


def modular_int_add(a: int, b: int, min_v: int = 1, max_v: int = 10) -> int:
    """Integer addition with wrapping values.

    Example:
    >>> [modular_int_add(5, i, 1, 10) for i in range(10)]
    [5, 6, 7, 8, 9, 10, 1, 2, 3, 4]
    >>> [modular_int_add(5, i, 2, 10) for i in range(10)]
    [5, 6, 7, 8, 9, 10, 2, 3, 4, 5]
    """
    return (a - min_v + b) % (max_v - min_v + 1) + min_v


class Player:
    def __init__(self, num: int, location: int):
        self.num = num
        self.location = location
        self.score = 0

    def move_roll(self, die: Die):
        rolls: list[int] = []
        for _ in range(3):
            rolls.append(die.get_roll())

        new_location = modular_int_add(self.location, sum(rolls))
        self.score += new_location
        self.location = new_location

    @property
    def is_winner(self) -> bool:
        return self.score >= 1000


WorldState = namedtuple("WorldState", ["p1_loc", "p1_score", "p2_loc", "p2_score"])


def prune_winners(state_dict: Counter[WorldState, int], winning_count: tuple[int, int]) -> Counter[WorldState, int]:
    state_dict_copy = state_dict.copy()
    for state in state_dict:
        if state.p1_score >= 21:
            winning_count[0] += state_dict[state]
            del state_dict_copy[state]
        elif state.p2_score >= 21:
            winning_count[1] += state_dict[state]
            del state_dict_copy[state]
    return state_dict_copy


def transition_state(state: WorldState, state_dict: Counter[WorldState, int], pnum: int):
    state_dict_new = Counter()
    for state in state_dict:
        sent = state_dict[state]
        if sent == 0:
            continue

        for r1, r2, r3 in product(range(1, 3 + 1), repeat=3):
            rsum = r1 + r2 + r3
            location1, score1, location2, score2 = state
            if pnum == 0:
                location1 = modular_int_add(location1, rsum)
                score1 += location1
            else:
                location2 = modular_int_add(location2, rsum)
                score2 += location2

            new_state = WorldState(location1, score1, location2, score2)
            state_dict_new[new_state] += sent
    return state_dict_new


def solve_a(s: str) -> int:
    (_, p1_start), (_, p2_start) = re.findall(r"Player (\d+) starting position: (\d+)", s)
    players = [Player(1, location=int(p1_start)), Player(2, location=int(p2_start))]

    die = DeterministicDie()

    for player in cycle(players):
        player.move_roll(die)
        if player.is_winner:
            winner = player
            break

    loser = players[winner.num % 2]

    return loser.score * die.roll_count


def solve_b(s: str) -> int:
    (_, p1_start), (_, p2_start) = re.findall(r"Player (\d+) starting position: (\d+)", s)
    p1, p2 = [Player(1, location=int(p1_start)), Player(2, location=int(p2_start))]

    state = WorldState(p1.location, p1.score, p2.location, p2.score)
    print(f"Initial state is: {state}")
    state_dict: Counter[WorldState, int] = Counter()
    state_dict[state] = 1
    winning_count: list[int] = [0, 0]

    for turn in range(14):
        for player_turn in range(2):
            state_dict = transition_state(state, state_dict, player_turn)
            state_dict = prune_winners(state_dict, winning_count)

    return max(winning_count)

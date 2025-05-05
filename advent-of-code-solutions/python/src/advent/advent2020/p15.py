class GameState:
    def __init__(self, values: list[int]):
        values = values.copy()
        self.turn_number = len(values)
        self.current_value = values.pop()
        self.last_turn = convert_list_to_last_turn_dict(values)

    def advance_game(self, n: int = 1):
        if n < 1:
            raise ValueError("n must be 1 or larger.")
        for _ in range(n):
            new_value = GameState.get_next_number(self.current_value, self.turn_number, self.last_turn)
            self.last_turn[self.current_value] = self.turn_number
            self.current_value = new_value
            self.turn_number += 1

    def get_nth_spoken_number(self, n: int) -> int:
        if n < self.turn_number:
            raise ValueError("n must be larger than the current turn number.")
        elif n == self.turn_number:
            return self.current_value
        else:
            self.advance_game(n - self.turn_number)
            return self.current_value

    @staticmethod
    def get_next_number(current_value: int, turn_number: int, last_turn: dict[int, int]):
        return turn_number - last_turn.get(current_value, turn_number)


def convert_list_to_last_turn_dict(lst: list[int]) -> dict[int, int]:
    return dict({v: i + 1 for i, v in enumerate(lst)})


def solve_a(s: str) -> int:
    puzzle_input = [int(x) for x in s.strip("\n").split(",")]
    return GameState(puzzle_input).get_nth_spoken_number(2020)


def solve_b(s: str) -> int:
    puzzle_input = [int(x) for x in s.strip("\n").split(",")]
    return GameState(puzzle_input).get_nth_spoken_number(30000000)


def test_get_next_number():
    gs = GameState([0, 3, 6])
    assert GameState.get_next_number(gs.current_value, gs.turn_number, gs.last_turn) == 0
    gs = GameState([0, 3, 6, 0])
    assert GameState.get_next_number(gs.current_value, gs.turn_number, gs.last_turn) == 3
    gs = GameState([0, 3, 6, 0, 3])
    assert GameState.get_next_number(gs.current_value, gs.turn_number, gs.last_turn) == 3
    gs = GameState([0, 3, 6, 0, 3, 3])
    assert GameState.get_next_number(gs.current_value, gs.turn_number, gs.last_turn) == 1
    gs = GameState([0, 3, 6, 0, 3, 3, 1])
    assert GameState.get_next_number(gs.current_value, gs.turn_number, gs.last_turn) == 0


def test_advance_game():
    gs = GameState([0, 3, 6])
    gs.advance_game(1)
    assert gs.current_value == 0
    gs.advance_game(1)
    assert gs.current_value == 3
    gs.advance_game(1)
    assert gs.current_value == 3
    gs.advance_game(1)
    assert gs.current_value == 1
    gs.advance_game(1)
    assert gs.current_value == 0
    gs.advance_game(1)
    assert gs.current_value == 4
    gs.advance_game(1)
    assert gs.current_value == 0


def test_get_nth_spoken_number():
    gs = GameState([0, 3, 6])
    assert gs.get_nth_spoken_number(3) == 6
    assert gs.get_nth_spoken_number(6) == 3
    assert gs.get_nth_spoken_number(7) == 1
    assert gs.get_nth_spoken_number(2020) == 436
    assert GameState([1, 3, 2]).get_nth_spoken_number(2020) == 1
    assert GameState([2, 1, 3]).get_nth_spoken_number(2020) == 10
    assert GameState([1, 2, 3]).get_nth_spoken_number(2020) == 27
    assert GameState([2, 3, 1]).get_nth_spoken_number(2020) == 78
    assert GameState([3, 2, 1]).get_nth_spoken_number(2020) == 438
    assert GameState([3, 1, 2]).get_nth_spoken_number(2020) == 1836

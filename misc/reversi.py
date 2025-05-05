# /// script
# requires-python = ">=3.11"
# dependencies = [
#     "numpy",
#     "typer",
# ]
# ///
"""Reversi Game Logic.

I wrote this to get an achievement in Her Story that requires you to get a draw
in the Mirror Game mini-game. The logic of the Mirror Game is similar to Reversi
(see https://en.wikipedia.org/wiki/Reversi) except:

- the first move is randomized (as opposed to always black),
- instead of ending when one player has no moves, the game continues, allowing
  the other player to make a move.

The program here just generates random games until it finds one that ends in a
draw and then prints out the moves.
"""

from itertools import product

import numpy as np
import typer


class Reversi:
    """
    >>> r = Reversi()
    >>> print(r)
    [[ 0  0  0  0  0  0  0  0]
     [ 0  0  0  0  0  0  0  0]
     [ 0  0  0  0  0  0  0  0]
     [ 0  0  0  1 -1  0  0  0]
     [ 0  0  0 -1  1  0  0  0]
     [ 0  0  0  0  0  0  0  0]
     [ 0  0  0  0  0  0  0  0]
     [ 0  0  0  0  0  0  0  0]]
    >>> r.make_move(5, 3)
    >>> print(r)
    [[ 0  0  0  0  0  0  0  0]
     [ 0  0  0  0  0  0  0  0]
     [ 0  0  0  0  0  0  0  0]
     [ 0  0  0  1 -1  0  0  0]
     [ 0  0  0  1  1  0  0  0]
     [ 0  0  0  1  0  0  0  0]
     [ 0  0  0  0  0  0  0  0]
     [ 0  0  0  0  0  0  0  0]]
    """

    def __init__(self, turn: int = 1):
        self.board = np.zeros((8, 8), dtype=np.int8)
        self.board[3, 3] = 1
        self.board[4, 4] = 1
        self.board[3, 4] = -1
        self.board[4, 3] = -1
        self.turn = turn
        self.moves = []

    def get_board(self):
        return self.board

    def get_turn(self):
        return self.turn

    def get_legal_moves(self):
        moves = []
        for i, j in product(range(8), repeat=2):
            if self.board[i, j] == 0 and self._is_legal_move(i, j):
                moves.append((i, j))
        return moves

    def _is_legal_move(self, i, j):
        # Current space must be empty.
        if self.board[i, j] != 0:
            return False
        for di, dj in product(range(-1, 2), repeat=2):
            if di == 0 and dj == 0:
                continue
            if self._is_legal_move_direction(i, j, di, dj):
                return True
        return False

    def _is_legal_move_direction(self, i, j, di, dj):
        # Current space must be empty.
        if self.board[i, j] != 0:
            return False
        # Move must be in bounds.
        if not (0 <= i + di < 8 and 0 <= j + dj < 8):
            return False
        # First step in the given direction can't be empty.
        if self.board[i + di, j + dj] == 0:
            return False
        # First step in the given direction must be the opponent's.
        if self.board[i + di, j + dj] == self.turn:
            return False
        # Look for a friendly piece in the given direction.
        for k in range(2, 8):
            # Move must be in bounds.
            if not (0 <= i + k * di < 8 and 0 <= j + k * dj < 8):
                break
            # If we find an empty space before finding a friendly piece, the move is illegal.
            if self.board[i + k * di, j + k * dj] == 0:
                return False
            # If we find a friendly piece, the move is legal.
            if self.board[i + k * di, j + k * dj] == self.turn:
                return True
        return False

    def make_move(self, i, j):
        if not self._is_legal_move(i, j):
            raise ValueError("Illegal move")
        for di, dj in product(range(-1, 2), repeat=2):
            if di == 0 and dj == 0:
                continue
            self._make_move_direction(i, j, di, dj)
        self.board[i, j] = self.turn
        self.turn *= -1
        self.moves.append((i, j))

    def _make_move_direction(self, i, j, di, dj):
        if not self._is_legal_move_direction(i, j, di, dj):
            return
        for k in range(1, 8):
            # Move must be in bounds.
            if not (0 <= i + k * di < 8 and 0 <= j + k * dj < 8):
                break
            # If we find a friendly piece, the move is legal.
            if self.board[i + k * di, j + k * dj] == self.turn:
                for l in range(1, k):
                    self.board[i + l * di, j + l * dj] = self.turn
                break

    def is_game_over(self):
        return len(self.get_legal_moves()) == 0

    def get_score(self):
        return np.sum(self.board)

    def get_score_black(self):
        return np.sum(self.board == 1)

    def get_score_white(self):
        return np.sum(self.board == -1)

    def get_winner(self):
        score = self.get_score()
        if score > 0:
            return 1
        elif score < 0:
            return -1
        else:
            return 0

    def __repr__(self):
        return str(self.board)

    def get_random_move(self):
        legal_moves = self.get_legal_moves()
        return legal_moves[np.random.randint(len(legal_moves))]

    def make_random_move(self):
        self.make_move(*self.get_random_move())

    def get_random_game(self, turn: int = 1):
        game = Reversi(turn=turn)
        while not game.is_game_over():
            game.make_random_move()
        return game

    def get_moves(self):
        return self.moves

    def get_random_draw_game_full_board(self, turn: int = 1):
        """This will get you the solution to the Her Story achievement."""
        r = Reversi()
        g = r.get_random_game()
        while True:
            g = Reversi().get_random_game(turn=turn)
            if g.get_score() == 0 and not (g.board == 0).any():
                break

        return g

    def get_moves_readable(self):
        return np.array([(x + 1, y + 1) for x, y in self.get_moves()])


def main(
    turn: int = typer.Option(
        1, help="1 if red (Reversi black) goes first, -1 if purple goes first."
    ),
):
    r = Reversi()
    g = r.get_random_draw_game_full_board(turn)
    print("Here is the final board:")
    print(g.get_board())
    print("Here are the moves (indexed from 1):")
    print(g.get_moves_readable())


if __name__ == "__main__":
    typer.run(main)

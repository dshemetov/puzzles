"""Shark Game Solver

This is a game in Dave the Diver. It is a variant of
[Nim](https://en.wikipedia.org/wiki/Nim#The_subtraction_game). The rules are as
follows:

1. The game starts with a number of shark's teeth (usually 20).
2. One of the teeth is marked at the start.
3. Two players take turns removing 1, 2, or 3 teeth from the pile.
4. The player who removes the marked tooth loses.

There is often a winning strategy for the player who goes first.

Let's begin with an example with the 6th tooth marked. The first player can win
by removing 1 tooth and then removing 4 - n, where n is the number of teeth the
second player removes.

Now let's consider the game with the 5th tooth marked. The second player has a
winning strategy in this case: if the first player removes n teeth, the second
player removes 4 - n. This will force the first player to remove the last tooth.

In general, if the marked tooth has index m (starting from 0), the first player
can win by removing m % 4 teeth, if m % 4 != 0, and otherwise the second player
has a winning strategy. The goal for each player is the same: make sure the
other player starts on a tooth with index i such that i % 4 = m % 4 and then
keep them there.

Going over the example with 6 teeth again, let's keep track of the modulo of the
index of the teeth:

    0 1 2 3 4 5
    0 1 2 3 0 1

Since the modulo of the marked tooth 5 % 4 is 1, the first player can win by
removing 1 tooth to make sure the second player starts at 1 % 4 = 1. However, if
the 5th tooth is marked, then

    0 1 2 3 4
    0 1 2 3 0

In this case, the first player already starts on the losing position, which
gives the second player the winning strategy of 4 - n.

PE301. Nim https://projecteuler.net/problem=301
"""

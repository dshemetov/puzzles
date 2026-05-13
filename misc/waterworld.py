"""Turing Complete - Waterworld

A puzzle for the Turing Complete game.
"""

from typing import List


def waterworld(s: List[int]) -> int:
    """Find the volume of water in this 2D world.

    Rules:
    - The world is represented by a 2D array of integers, where the value at each index represents the height of the terrain.
    - The world is surrounded by a wall of height 0.
    - The world can have multiple bodies of water, where each body of water is represented by a region of contiguous water cells.

    Examples:
    >>> waterworld([int(x) for x in "4614 6514 1265 6142" if x != " "])
    28
    >>> waterworld([int(x) for x in "2152 4666 4561 4223" if x != " "])
    13
    """
    n = len(s)
    arr1 = [0] * n
    m = 0
    for i in range(n):
        m = max(m, s[i])
        arr1[i] = m - s[i]
    arr2 = [0] * n
    m = 0
    for i in range(n - 1, -1, -1):
        m = max(m, s[i])
        arr2[i] = m - s[i]
    water = 0
    for i in range(n):
        water += min(arr1[i], arr2[i])
    return water

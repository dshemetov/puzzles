from collections import defaultdict


def p1345b(arr: list[int]) -> int:
    """1345. Jump Game IV https://leetcode.com/problems/jump-game-iv/

    The BFS solution.

    Examples
    --------
    >>> p1345b([100, -23, -23, 404, 100, 23, 23, 23, 3, 404])
    3
    >>> p1345b([7])
    0
    >>> p1345b([7, 6, 9, 6, 9, 6, 9, 7])
    1
    >>> p1345b([7, 7, 2, 1, 7, 7, 7, 3, 4, 1])
    3

    """
    if len(arr) == 1:
        return 0

    value_ix = defaultdict(list)
    for ix, val in enumerate(arr):
        value_ix[val].append(ix)

    seen = {0}
    cur = [0]
    step = 0

    while cur:
        nex = []

        for ix in cur:
            if ix == len(arr) - 1:
                return step

            for ix_ in [ix - 1, ix + 1] + value_ix[arr[ix]]:
                if 0 <= ix_ < len(arr) and ix_ not in seen:
                    nex.append(ix_)
                    seen.add(ix_)

            del value_ix[arr[ix]]

        cur = nex
        step += 1

    return -1

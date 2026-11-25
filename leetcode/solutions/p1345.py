from collections import defaultdict
from queue import PriorityQueue


def p1345(arr: list[int]) -> int:
    """1345. Jump Game IV https://leetcode.com/problems/jump-game-iv/

    Lessons learned:
    - This solution is very similar to Jump Game III. I added a priority queue,
    but this problem could be done with BFS as well.

    Examples
    --------
    >>> p1345([100, -23, -23, 404, 100, 23, 23, 23, 3, 404])
    3
    >>> p1345([7])
    0
    >>> p1345([7, 6, 9, 6, 9, 6, 9, 7])
    1
    >>> p1345([7, 7, 2, 1, 7, 7, 7, 3, 4, 1])
    3

    """
    if len(arr) == 1:
        return 0

    value_ix = defaultdict(list)
    for ix, val in enumerate(arr):
        value_ix[val].append(ix)

    seen = set()
    queue = PriorityQueue()
    queue.put((0, 0))
    while queue:
        jumps, ix = queue.get()

        if ix == len(arr) - 1:
            return jumps

        seen.add(ix)

        for ix_ in [ix + 1, ix - 1] + value_ix[arr[ix]]:
            if 0 <= ix_ < len(arr) and ix_ not in seen:
                queue.put((jumps + 1, ix_))

        del value_ix[arr[ix]]

    return -1

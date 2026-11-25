from collections import defaultdict


def p1(nums: list[int], target: int) -> list[int]:
    """1. Two Sum https://leetcode.com/problems/two-sum/

    Examples
    --------
    >>> p1([3, 3], 6)
    [0, 1]
    >>> p1([3, 2, 4], 7)
    [0, 2]

    """
    ix_map = defaultdict(list)
    for i, x in enumerate(nums):
        ix_map[x].append(i)

    for x in ix_map:
        if ix_map.get(target - x):
            if x == target - x and len(ix_map[x]) == 2:
                return ix_map[target - x]
            if x != target - x:
                return [ix_map[x][0], ix_map[target - x][0]]
    return []

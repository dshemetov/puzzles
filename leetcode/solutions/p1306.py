def p1306(arr: list[int], start: int) -> bool:
    """1306. Jump Game III https://leetcode.com/problems/jump-game-iii/

    Just a BFS.

    Examples
    --------
    >>> p1306([4, 2, 3, 0, 3, 1, 2], 5)
    True
    >>> p1306([4, 2, 3, 0, 3, 1, 2], 0)
    True
    >>> p1306([3, 0, 2, 1, 2], 2)
    False

    """
    seen = set()
    stack = {start}
    while stack:
        ix = stack.pop()

        if arr[ix] == 0:
            return True

        seen.add(ix)

        for ix_ in [ix + arr[ix], ix - arr[ix]]:
            if 0 <= ix_ < len(arr) and ix_ not in seen:
                stack.add(ix_)

    return False

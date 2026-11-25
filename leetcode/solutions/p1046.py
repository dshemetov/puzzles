from bisect import insort


def p1046(stones: list[int]) -> int:
    """1046. Last Stone Weight https://leetcode.com/problems/last-stone-weight/

    Examples
    --------
    >>> p1046([2, 7, 4, 1, 8, 1])
    1
    >>> p1046([1, 3])
    2
    >>> p1046([1])
    1

    """
    sorted_stones = sorted(stones)
    while len(sorted_stones) > 1:
        a, b = sorted_stones.pop(), sorted_stones.pop()
        if a != b:
            insort(sorted_stones, a - b)
    return sorted_stones[0] if sorted_stones else 0

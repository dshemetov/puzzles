def p167(numbers: list[int], target: int) -> list[int]:
    """167. Two Sum II - Input Array Is Sorted https://leetcode.com/problems/two-sum-ii-input-array-is-sorted/

    Examples
    --------
    >>> p167([2, 7, 11, 15], 9)
    [1, 2]
    >>> p167([2, 3, 4], 6)
    [1, 3]
    >>> p167([-1, 0], -1)
    [1, 2]

    """
    lo, hi = 0, len(numbers) - 1
    while lo < hi:
        s = numbers[lo] + numbers[hi]
        if s < target:
            lo += 1
        elif s > target:
            hi -= 1
        else:
            return [lo + 1, hi + 1]
    return [0]

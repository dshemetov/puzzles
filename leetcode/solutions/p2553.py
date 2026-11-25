def p2553(nums: list[int]) -> list[int]:
    """2553. Separate the Digits in an Array https://leetcode.com/problems/separate-the-digits-in-an-array

    Examples
    --------
    >>> p2553([13, 25, 83, 77])
    [1, 3, 2, 5, 8, 3, 7, 7]
    >>> p2553([7, 1, 3, 9])
    [7, 1, 3, 9]

    """
    return [int(y) for x in nums for y in str(x)]

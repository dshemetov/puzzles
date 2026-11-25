def p977(nums: list[int]) -> list[int]:
    """977. Squares of a Sorted Array https://leetcode.com/problems/squares-of-a-sorted-array/

    Examples
    --------
    >>> p977([-4, -1, 0, 3, 10])
    [0, 1, 9, 16, 100]
    >>> p977([-7, -3, 2, 3, 11])
    [4, 9, 9, 49, 121]
    >>> p977([-5, -3, -2, -1])
    [1, 4, 9, 25]

    """
    le, ri = 0, len(nums) - 1
    res = [0] * len(nums)
    i = len(nums) - 1
    while le <= ri:
        left, right = nums[le] ** 2, nums[ri] ** 2
        if left > right:
            res[i] = left
            le += 1
        else:
            res[i] = right
            ri -= 1
        i -= 1

    return res

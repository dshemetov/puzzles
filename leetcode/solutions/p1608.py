def p1608(nums: list[int]) -> int:
    """1608. Special Array With X Elements Greater Than or Equal X https://leetcode.com/problems/special-array-with-x-elements-greater-than-or-equal-x

    Examples
    --------
    >>> p1608([3, 5])
    2
    >>> p1608([0, 0])
    -1
    >>> p1608([0, 4, 3, 0, 4])
    3

    """
    nums.sort()
    lo, hi = 0, len(nums)
    while lo <= hi:
        x = (hi + lo) // 2
        i = 0
        while i < len(nums) and nums[i] < x:
            i += 1
        if x == len(nums) - i:
            return x
        if x > len(nums) - i:
            hi -= 1
        if x < len(nums) - i:
            lo += 1
    return -1

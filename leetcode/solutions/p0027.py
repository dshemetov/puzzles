def p27(nums: list[int], val: int) -> int:
    """27. Remove Element https://leetcode.com/problems/remove-element

    Examples
    --------
    >>> p27([3, 2, 2, 3], 3)
    2
    >>> p27([0, 1, 2, 2, 3, 0, 4, 2], 2)
    5

    """
    n = len(nums)
    k = 0
    for i in range(n):
        if nums[i] != val:
            nums[k] = nums[i]
            k += 1
    return k

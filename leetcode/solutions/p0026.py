def p26(nums: list[int]) -> int:
    """26. Remove Duplicates from Sorted Array https://leetcode.com/problems/remove-duplicates-from-sorted-array/

    Examples
    --------
    >>> p26([1, 1, 2])
    2
    >>> p26([0, 0, 1, 1, 1, 2, 2, 3, 3, 4])
    5

    """
    k = 0
    for i in range(1, len(nums)):
        if nums[k] != nums[i]:
            k += 1
            nums[k] = nums[i]
    return k + 1

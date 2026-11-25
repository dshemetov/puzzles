def p33(nums: list[int], target: int) -> int:
    """33. Search in Rotated Sorted Array https://leetcode.com/problems/search-in-rotated-sorted-array/

    Approach: find the shift index using binary search, then do a regular binary
    search, translating indices.

    Some worked examples:

    34567012

    lo  hi  mid
    0   7   3
    3   7   5
    3   5   4

    lo = 5, hi = 4

    01234567

    lo = 0, hi = 7

    12345670

    lo  hi  mid
    0   7   3
    3   7   5
    5   7   6

    lo = 7, hi = 6

    70123456

    lo  hi  mid
    0   7   3
    0   3   1

    lo = 1, hi = 0

    01234567, 2

    lo  hi  mid
    0   7   3
    0   3   1
    1   3   2

    Examples
    --------
    >>> p33([4, 5, 6, 7, 0, 1, 2], 0)
    4
    >>> p33([4, 5, 6, 7, 0, 1, 2], 3)
    -1
    >>> p33([1], 0)
    -1
    >>> p33([4, 5, 1, 2, 3], 1)
    2
    >>> p33([5, 1, 3], 5)
    0

    """
    lo, hi = 0, len(nums) - 1
    if nums[lo] > nums[hi]:
        while lo + 1 < hi:
            mid = (lo + hi) // 2

            if nums[mid] < nums[hi]:
                hi = mid
            elif nums[lo] < nums[mid]:
                lo = mid
        s = hi
    else:
        s = 0

    lo, hi = 0, len(nums)
    while lo <= hi:
        mid = (lo + hi) // 2
        ix = (s + mid) % len(nums)

        if nums[ix] == target:
            return ix
        if nums[ix] > target:
            hi = mid - 1
        if nums[ix] < target:
            lo = mid + 1
    return -1

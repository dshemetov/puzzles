def p34(nums: list[int], target: int) -> list[int]:
    """
    Examples:
    >>> p34([5, 7, 7, 8, 8, 10], 8)
    [3, 4]
    >>> p34([5, 7, 7, 8, 8, 10], 6)
    [-1, -1]
    >>> p34([], 0)
    [-1, -1]
    >>> p34([5, 7, 7, 7, 7, 7, 8, 8, 8, 8, 8, 10, 100], 8)
    [6, 10]
    >>> p34([1], 0)
    [-1, -1]
    >>> p34([2, 2], 2)
    [0, 1]
    >>> p34([1, 3], 1)
    [0, 0]
    >>> p34([2, 2], 1)
    [-1, -1]
    >>> p34([1, 4], 4)
    [1, 1]
    """
    if not nums:
        return [-1, -1]
    if len(nums) == 1:
        return [0, 0] if nums[0] == target else [-1, -1]

    lo, hi = 0, len(nums) - 1
    while lo <= hi:
        mid = (lo + hi) // 2
        if nums[mid] < target:
            lo = mid + 1
        if nums[mid] == target:
            break
        if nums[mid] > target:
            hi = mid - 1

    if nums[mid] != target:
        return [-1, -1]

    lo = mid
    d = 1
    while True:
        lo -= d
        if lo > 0 and nums[lo] == target:
            d *= 2
        elif lo == 0 and nums[lo] == target:
            break
        elif d == 1:
            lo += 1
            break
        else:
            lo += d
            d = 1

    hi = mid
    d = 1
    while True:
        hi += d
        if hi < len(nums) and nums[hi] == target:
            d *= 2
        elif hi == 0 and nums[hi] == target:
            break
        elif d == 1:
            hi -= 1
            break
        else:
            hi -= d
            d = 1

    return [lo, hi]

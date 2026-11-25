def p35(nums: list[int], target: int) -> int:
    """35. Search Insert Position https://leetcode.com/problems/search-insert-position

    Examples
    --------
    >>> p35([1, 3, 5, 6], 5)
    2
    >>> p35([1, 3, 5, 6], 2)
    1
    >>> p35([1, 3, 5, 6], 7)
    4

    """
    for i, x in enumerate(nums):
        if target <= x:
            return i
    return len(nums)

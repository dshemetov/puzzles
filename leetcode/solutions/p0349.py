def p349(nums1: list[int], nums2: list[int]) -> list[int]:
    """349. Intersection of Two Arrays https://leetcode.com/problems/intersection-of-two-arrays

    Examples
    --------
    >>> p349([1, 2, 2, 1], [2, 2])
    [2]
    >>> p349([4, 9, 5], [9, 4, 9, 8, 4])
    [9, 4]

    """
    return list(set(nums1) & set(nums2))

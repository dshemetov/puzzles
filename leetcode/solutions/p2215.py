def p2215(nums1: list[int], nums2: list[int]) -> list[list[int]]:
    """2215. Find the Difference of Two Arrays https://leetcode.com/problems/find-the-difference-of-two-arrays/

    Examples
    --------
    >>> p2215([1, 2, 3], [2, 4, 6])
    [[1, 3], [4, 6]]
    >>> p2215([1, 2, 3, 3], [1, 1, 2, 2])
    [[3], []]

    """
    s1, s2 = set(nums1), set(nums2)
    return [[n for n in s1 if n not in s2], [n for n in s2 if n not in s1]]

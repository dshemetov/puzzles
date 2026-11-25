def p31(nums: list[int]) -> None:
    """31. Next Permutation https://leetcode.com/problems/next-permutation

    Learned a lot about permutations. The algorithm used traces back to Narayana
    Pandita.

    One-line notation   Cycle notation  Swaps from previous
    1234                ()              ()
    1243                (34)            (34)
    1324                (23)            (34)(23)
    1342                (234)           (34)
    1423                (243)           (23)(34)
    1432                (24)            (34)
    2134                (12)            (34)(23)(12)(34)
    2143                (12)(34)        (34)
    2314                (123)           (34)(23)
    2341                (1234)          (34)
    2413                (1243)          (23)(34)
    2431                (124)           (34)
    3124                (132)           (23)(12)(34)(23)
    3142                (1342)          (34)
    3214                (13)            (34)(23)(12)
    3241                (134)
    3412                (13)(24)
    3421                (1324)
    4123                (1432)
    4132                (142)
    4213                (143)
    4231                (14)
    4312                (1423)
    4321                (14)(23)

    Factorial number system (up to 4! - 1):
    (000)   0
    (001)   1
    (010)   2
    (011)   3
    (020)   4
    (021)   5
    (100)   6
    (101)   7
    (110)   8
    (111)   9
    (120)   10
    (121)   11
    (200)   12
    (201)   13
    (210)   14
    (211)   15
    (220)   16
    (221)   17
    (300)   18
    (301)   19
    (310)   20
    (311)   21
    (320)   22
    (321)   23

    References
    ----------
    https://en.wikipedia.org/wiki/Permutation#One-line_notation
    https://en.wikipedia.org/wiki/Permutation#Cycle_notation
    https://en.wikipedia.org/wiki/Permutation#Numbering_permutations

    Examples
    --------
    >>> nums = [1, 2, 3]
    >>> p31(nums)
    >>> nums
    [1, 3, 2]
    >>> nums = [3, 2, 1]
    >>> p31(nums)
    >>> nums
    [1, 2, 3]
    >>> nums = [1, 1, 5]
    >>> p31(nums)
    >>> nums
    [1, 5, 1]
    >>> nums = [1, 2, 3, 4]
    >>> p31(nums)
    >>> nums
    [1, 2, 4, 3]
    >>> nums = [1, 3, 4, 2]
    >>> p31(nums)
    >>> nums
    [1, 4, 2, 3]

    """
    n = len(nums)
    # Find the largest index k1 such that nums[k1] < nums[k1 + 1]
    k1 = -1
    for i in range(n - 1):
        if nums[i] < nums[i + 1]:
            k1 = max(i, k1)
    # If not found, then the permutation is the last one
    if k1 == -1:
        nums.reverse()
        return
    # Find the largest index k2 such that nums[k1] < nums[k2]
    k2 = k1
    for j in range(k1 + 1, n):
        if nums[k1] < nums[j]:
            k2 = max(j, k2)
    # Swap
    nums[k1], nums[k2] = nums[k2], nums[k1]
    # Reverse the array
    lo, hi = k1 + 1, n - 1
    while lo < hi:
        nums[lo], nums[hi] = nums[hi], nums[lo]
        lo += 1
        hi -= 1

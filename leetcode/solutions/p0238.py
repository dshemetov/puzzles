def p238(nums: list[int]) -> list[int]:
    """238. Product of Array Except Self https://leetcode.com/problems/product-of-array-except-self

    Examples
    --------
    >>> p238([1, 2, 3, 4])
    [24, 12, 8, 6]
    >>> p238([1, 2, 3, 4, 5])
    [120, 60, 40, 30, 24]
    >>> p238([-1, 1, 0, -3, 3])
    [0, 0, 9, 0, 0]

    """
    n = len(nums)
    prefix_products = [1] * n
    suffix_products = [1] * n
    for i in range(1, n):
        prefix_products[i] = prefix_products[i - 1] * nums[i - 1]
    for i in range(n - 2, -1, -1):
        suffix_products[i] = suffix_products[i + 1] * nums[i + 1]

    return [prefix_products[i] * suffix_products[i] for i in range(n)]

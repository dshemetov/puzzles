def p1674(nums: list[int], limit: int) -> int:
    """1674. Minimum Moves to Make Array Complementary https://leetcode.com/problems/minimum-moves-to-make-array-complementary/

    You can reason out that for all T on the number line, the cost to convert
    all pairs to the number T is:

    cost(T) = sum(
        0 if T = x + y
        1 if min(x, y) <= T <= max(x, y) + limit
        2 otherwise
        for x, y in pairs)

    So we need to scan through all 1 <= T <= 2 * limit + 2 to find the minimum
    cost. We can do this in O(n) by using a difference array. In this problem,
    the size of the array isn't very large, so not using a sparse representation
    is fine.

    Examples
    --------
    >>> p1674([1, 2, 4, 3], 4)
    1
    >>> p1674([1, 2, 2, 1], 2)
    2
    >>> p1674([1, 2, 1, 2], 2)
    0

    """
    n = len(nums)
    n_pairs = n // 2
    pairs = [(nums[i], nums[n - i - 1]) for i in range(n_pairs)]
    intervals = [(min(x, y) + 1, max(x, y) + limit) for x, y in pairs]
    # print(pairs)
    # print(intervals)
    count_map = [0] * (2 * limit + 2)
    for i in range(n_pairs):
        a, b = pairs[i]
        L, R = intervals[i]
        count_map[L] += 1
        count_map[R + 1] -= 1
        count_map[a + b] += 1
        count_map[a + b + 1] -= 1

    # print(count_map)

    result = 0
    for j in range(1, len(count_map)):
        count_map[j] += count_map[j - 1]
        result = max(result, count_map[j])

    return n - result

from collections import defaultdict


def p560(nums: list[int], k: int) -> int:
    """560. Subarray Sum Equals K https://leetcode.com/problems/subarray-sum-equals-k/

    Same as 930.

    Examples
    --------
    >>> p560([1, 1, 1], 2)
    2
    >>> p560([1, 2, 3], 3)
    2

    """
    goal = k
    prefix_sum = 0
    count = 0
    prefix_sum_counts = defaultdict(int)
    for num in nums:
        prefix_sum += num
        if prefix_sum == goal:
            count += 1
        count += prefix_sum_counts[prefix_sum - goal]
        prefix_sum_counts[prefix_sum] += 1
    return count

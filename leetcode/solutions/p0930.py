from collections import defaultdict


def p930(nums: list[int], goal: int) -> int:
    """930. Binary Subarrays With Sum https://leetcode.com/problems/binary-subarrays-with-sum

    Same as 560.

    Lessons learned:
    - The solution relies on prefix sums, which is a common technique for
    counting subarrays with a certain sum. The prefix sum is the cumulative sum
    of the elements up to a given point. As we run through the array, we can
    look up how many times the prefix sum was equal to the difference between
    the current prefix sum and the goal and add that to the count. This is
    because starting from that point and ending at the current point, the prefix
    sum will be

        prefix_sum - (prefix_sum - goal) = goal

    Examples
    --------
    >>> p930([1, 0, 1, 0, 1], 2)
    4
    >>> p930([0, 0, 0, 0, 0], 0)
    15
    >>> p930([1, 1, 1, 1, 1], 1)
    5

    """
    prefix_sum = 0
    count = 0
    prefix_sum_counts = defaultdict(int)
    prefix_sum_counts[0] = 1
    for num in nums:
        prefix_sum += num
        count += prefix_sum_counts[prefix_sum - goal]
        prefix_sum_counts[prefix_sum] += 1
    return count

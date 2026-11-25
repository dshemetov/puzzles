from collections import Counter


def p347(nums: list[int], k: int) -> list[int]:
    """347. Top K Frequent Elements https://leetcode.com/problems/top-k-frequent-elements/

    Examples
    --------
    >>> p347([1, 1, 1, 2, 2, 3], 2)
    [1, 2]
    >>> p347([1], 1)
    [1]

    """
    c = Counter(nums)
    return [num for num, _ in c.most_common(k)]

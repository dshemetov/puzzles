from heapq import heappop, heappush


def p373(nums1: list[int], nums2: list[int], k: int) -> list[list[int]]:
    """373. Find K Pairs with Smallest Sums https://leetcode.com/problems/find-k-pairs-with-smallest-sums/

    Examples
    --------
    >>> p373([1, 7, 11], [2, 4, 6], 3)
    [[1, 2], [1, 4], [1, 6]]
    >>> p373([1, 1, 2], [1, 2, 3], 2)
    [[1, 1], [1, 1]]
    >>> p373([1, 2], [3], 3)
    [[1, 3], [2, 3]]
    >>> p373([1, 2, 4, 5, 6], [3, 5, 7, 9], 3)
    [[1, 3], [2, 3], [1, 5]]
    >>> p373([1, 5, 10], [2, 7, 9], 6)
    [[1, 2], [5, 2], [1, 7], [1, 9], [5, 7], [10, 2]]

    """
    if not nums1 or not nums2:
        return []

    pairs = []
    heap = [[nums1[0] + nums2[0], 0, 0]]
    visited = set()

    while len(pairs) < k and heap:
        _, i, j = heappop(heap)
        if (i, j) in visited:
            continue
        pairs.append([nums1[i], nums2[j]])
        visited.add((i, j))
        if i + 1 < len(nums1):
            heappush(heap, [nums1[i + 1] + nums2[j], i + 1, j])
        if j + 1 < len(nums2):
            heappush(heap, [nums1[i] + nums2[j + 1], i, j + 1])

    return pairs

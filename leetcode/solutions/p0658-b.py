def p658b(arr: list[int], k: int, x: int) -> list[int]:
    """Examples
    >>> p658b([1, 2, 3, 4, 5], 4, 3)
    [1, 2, 3, 4]
    >>> p658b([1, 2, 3, 4, 5], 4, -1)
    [1, 2, 3, 4]
    >>> p658b([1, 2, 3, 4, 5], 4, 4)
    [2, 3, 4, 5]
    >>> p658b([1, 2, 3, 4, 5], 2, 4)
    [3, 4]
    >>> p658b([1, 2, 3, 3, 4, 5, 90, 100], 3, 4)
    [3, 3, 4]

    """
    lo, hi = 0, len(arr) - k
    while lo < hi:
        mid = (lo + hi) // 2
        # Equivalently x > (arr[mid] + arr[mid + k]) / 2
        if x - arr[mid] > arr[mid + k] - x:
            lo = mid + 1
        else:
            hi = mid
    return arr[lo : lo + k]

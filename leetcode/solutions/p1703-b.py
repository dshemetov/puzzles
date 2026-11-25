def get_gaps(nums: list[int]) -> list[int]:
    gaps = []
    prev = -1
    for i, x in enumerate(nums):
        if prev == -1 and x == 1:
            prev = i
        elif prev != -1 and x == 1:
            gaps.append(i - prev)
            prev = i
    return gaps


def p1703b(nums: list[int], k: int) -> int:
    """Examples
    >>> p1703b([1, 0, 0, 1, 0, 0], 2)
    2
    >>> p1703b([1, 0, 0, 1, 0, 1], 2)
    1
    >>> p1703b([1, 0, 0, 0, 0, 0, 1, 1], 3)
    5
    >>> p1703b([1, 1, 0, 1], 2)
    0
    >>> p1703b([0, 0, 0, 1, 0, 1, 1, 0, 1], 3)
    1
    >>> p1703b([0, 0, 0, 1, 0, 1, 1, 0, 1], 4)
    2
    >>> p1703b([1, 0, 1, 0, 1, 0, 0, 0, 1], 4)
    6

    """
    if len(nums) == k or k == 1:
        return 0

    def triangular_number(n: int) -> int:
        return n * (n + 1) // 2

    mid1, mid2 = k // 2 - 1, k // 2
    if k % 2 == 0:
        correction_factor = triangular_number(mid1) + triangular_number(mid2)
    else:
        correction_factor = 2 * triangular_number(mid2)

    def calc2(gaps: list, k: int, j: int) -> int:
        """Calculate using the absolute value formula with the differences between indices."""
        return sum(min(i + 1, k - (i + 1)) * gaps[j + i] for i in range(k - 1))

    gaps = get_gaps(nums)

    if len(gaps) == k - 1:
        return calc2(gaps, k, 0) - correction_factor

    m0, m1 = calc2(gaps, k, 0), calc2(gaps, k, 1)
    delta1 = m1 - m0
    m = min(m0, m1)

    for j in range(0, len(gaps) - k):
        if k % 2 == 1:
            delta2 = gaps[j] - gaps[j + k // 2] - gaps[j + k // 2 + 1] + gaps[j + k]
        else:
            delta2 = gaps[j] - 2 * gaps[j + k // 2] + gaps[j + k]
        delta1 = delta1 + delta2
        m1 = m1 + delta1
        m = min(m, m1)

    return m - correction_factor

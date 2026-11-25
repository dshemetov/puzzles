def get_median_sorted(nums: list[int]) -> float:
    if len(nums) == 1:
        return nums[0]

    mid = len(nums) // 2

    if len(nums) % 2 == 0:
        return (nums[mid] + nums[mid - 1]) / 2

    return nums[mid]


def p4(nums1: list[int], nums2: list[int]) -> float:
    """4. Median of Two Sorted Arrays https://leetcode.com/problems/median-of-two-sorted-arrays/

    Lessons learned:
    - I spent a long time thinking about this problem before looking it up.
    - We use the following notation in the code:

        A refers to the shorter array,
        B refers to the longer array,
        midA refers to a partition point in A,
        midB refers to a partition point in B,
        Aleft = A[midA - 1], refers to the largest element in the left partition of A
        Aright = A[midA], refers to the smallest element in the right partition of A
        Bleft = B[midB - 1], refers to the largest element in the left partition of B
        Bright = B[midB], refers to the smallest element in the right partition of B

    - The key insight is this:

        midA + midB = (len(A) + len(B) + 1) // 2,

      which implies

        midB = (len(A) + len(B) + 1) // 2 - midA.

      This means that we can find a even partition of the total set, by finding
      the partition point in just one array via binary search.

    - So our problem is solved if we can find a partition (midA, midB) with:

        len(A[:midA]) + len(B[:midB]) == len(A[midA:]) + len(B[midB:]),
        Aleft <= Bright,
        Bleft <= Aright.

    - The median is then

        median = max(Aleft, Bleft)                                if len(A) + len(B) odd
               = (max(Aleft, Bleft) + min(Aright, Bright)) / 2   else

    - Swapping two variables in Python swaps pointers under the hood:
      https://stackoverflow.com/a/62038590/4784655.

    Examples
    --------
    >>> p4([1, 3], [2])
    2.0
    >>> p4([1, 2], [3, 4])
    2.5
    >>> p4([1, 3], [2, 4])
    2.5
    >>> a1 = [5, 13, 15]
    >>> b1 = [0, 10, 10, 15, 20, 20, 25]
    >>> p4(a1, b1) == get_median_sorted(sorted(a1 + b1))
    True
    >>> a2 = [9, 36, 44, 45, 51, 67, 68, 69]
    >>> b2 = [7, 20, 26, 27, 30, 43, 54, 73, 76, 88, 91, 94]
    >>> p4(a2, b2) == get_median_sorted(sorted(a2 + b2))
    True
    >>> a2 = [2, 2, 2, 2, 2, 2, 5]
    >>> b2 = [0, 0, 0, 0, 0, 0, 0, 1, 6, 6, 6, 6, 6, 6, 6, 6, 6]
    >>> p4(a2, b2) == get_median_sorted(sorted(a2 + b2))
    True
    >>> a2 = [2, 2, 2, 4, 5, 7, 8, 9]
    >>> b2 = [1, 1, 1, 1, 1, 3, 6, 10, 11, 11, 11, 11]
    >>> p4(a2, b2) == get_median_sorted(sorted(a2 + b2))
    True

    """
    if not nums1:
        return get_median_sorted(nums2)
    if not nums2:
        return get_median_sorted(nums1)

    A, B = nums1, nums2

    if len(A) > len(B):
        A, B = B, A

    total = len(A) + len(B)
    lo, hi = 0, len(A)
    while True:
        midA = (lo + hi) // 2
        midB = (total + 1) // 2 - midA

        Aleft = A[midA - 1] if midA > 0 else float("-inf")
        Aright = A[midA] if midA < len(A) else float("inf")
        Bleft = B[midB - 1] if midB > 0 else float("-inf")
        Bright = B[midB] if midB < len(B) else float("inf")

        if Aleft <= Bright and Bleft <= Aright:
            if total % 2 == 0:
                return (max(Aleft, Bleft) + min(Aright, Bright)) / 2
            return float(max(Aleft, Bleft))

        if Aleft > Bright:
            hi = midA - 1
        else:
            lo = midA + 1

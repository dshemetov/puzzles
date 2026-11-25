def p1208(s: str, t: str, maxCost: int) -> int:
    """1208. Get Equal Substrings Within Budget https://leetcode.com/problems/get-equal-substrings-within-budget

    Lessons learned:
    * The toughest part was correctly handling indices. I used half-open [lo, hi) intervals for a while, but things turned out cleaner with closed intervals [lo, hi].
    * My first solution also shrunk the sliding window, until I realized that you don't need to.
    * Worked example:

    1010100100101, 2
    [0 0] 1
    [0 1] 1
    [0 2] 0
    [0 3] 0
    [1 3] 1
    [1 4] 0
    [1 5] 0
    [1 6] 0
    [2 6] 0
    [3 6] 1
    [3 7] 0
    [3 8] 0
    [3 9] 0
    [4 9] 0
    [5 9] 1
    [5 10] 0
    [5 11] 0
    [6 11] 0
    [7 11] 0
    [8 11] 1
    [9 12] 0

    Examples
    --------
    >>> p1208("abcd", "bcdf", 3)
    3
    >>> p1208("abcd", "cdef", 3)
    1
    >>> p1208("abcd", "acde", 0)
    1
    >>> p1208("ajte", "bjte", 3)
    4
    >>> p1208("abcd", "cdef", 1)
    0

    """
    diffs = [abs(ord(x) - ord(y)) for x, y in zip(s, t)]
    lo, hi, max_len = 0, 0, 0
    currCost = maxCost
    while hi < len(s):
        currCost -= diffs[hi]
        if currCost >= 0:
            max_len = max(max_len, hi - lo + 1)
        else:
            currCost += diffs[lo]
            lo += 1
        hi += 1
    return max_len

def p766(matrix: list[list[int]]) -> bool:
    """766. Toeplitz Matrix https://leetcode.com/problems/toeplitz-matrix/

    Examples
    --------
    >>> p766([[1, 2, 3, 4], [5, 1, 2, 3], [9, 5, 1, 2]])
    True
    >>> p766([[1, 2], [2, 2]])
    False
    >>> p766([[11, 74, 0, 93], [40, 11, 74, 7]])
    False

    """
    return all(
        r == 0 or c == 0 or matrix[r - 1][c - 1] == val for r, row in enumerate(matrix) for c, val in enumerate(row)
    )

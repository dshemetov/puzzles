def p46(nums: list) -> list[list]:
    """46. Permutations https://leetcode.com/problems/permutations/

    First attempt is the Steinhaus-Johnson-Trotter algorithm. Slow, but simple.

    Examples
    --------
    >>> sorted(p46([1, 2, 3]))
    [[1, 2, 3], [1, 3, 2], [2, 1, 3], [2, 3, 1], [3, 1, 2], [3, 2, 1]]
    >>> sorted(p46([0, 1]))
    [[0, 1], [1, 0]]
    >>> p46([1])
    [[1]]
    """
    permutations = []
    for x in nums:
        if not permutations:
            permutations.append([x])
        else:
            temp = [p[:i] + [x] + p[i:] for p in permutations for i in range(len(p) + 1)]
            permutations = temp

    return permutations

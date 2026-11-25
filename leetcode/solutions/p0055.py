def p55(nums: list[int]) -> bool:
    """55. Jump Game https://leetcode.com/problems/jump-game/

    Lessons learned:
    - The forward version of the dynamic programming solution is more intuitive,
    but it is slow. The backward version is much faster.
    - The second version is even better, avoiding the second for loop. The
    intuition there is that we keep track of minimum known index that can reach
    the end.

    Examples
    --------
    >>> p55([2, 3, 1, 1, 4])
    True
    >>> p55([3, 2, 1, 0, 4])
    False
    >>> p55(list(range(10, -1, -1)) + [0])
    False

    """
    n = len(nums)
    reachable = [0] * (n - 1) + [1]
    for i in range(n - 2, -1, -1):
        for j in range(i + 1, min(n, i + nums[i] + 1)):
            if reachable[j]:
                reachable[i] = 1
                break

    return reachable[0] == 1

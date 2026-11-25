def p45(nums: list[int]) -> int:
    """45. Jump Game II https://leetcode.com/problems/jump-game-ii/

    Lessons learned:
    - This is the backward version of the dynamic programming solution from
    problem 55 Jump Game, except here we keep track of the move counts.
    - It turns out that the greedy solution is optimal. The intuition is that we
    always want to jump to the farthest reachable index. The proof is by
    contradiction. Suppose we have a better solution that jumps to a closer
    index. Then we can always replace that jump with a jump to the farthest
    reachable index, and the new solution will be at least as good as the
    original one. The only necessary jumps are the ones that allow a new
    farthest index to be reached.

    Examples
    --------
    >>> p45([2, 3, 1, 1, 4])
    2
    >>> p45([2, 3, 0, 1, 4])
    2

    """
    n = len(nums)
    reachable = [0] * (n - 1) + [1]
    for i in range(n - 2, -1, -1):
        for j in range(i + 1, min(n, i + nums[i] + 1)):
            if reachable[j]:
                reachable[i] = min(1 + reachable[j], reachable[i]) if reachable[i] != 0 else 1 + reachable[j]

    return reachable[0] - 1

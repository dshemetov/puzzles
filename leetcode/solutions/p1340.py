def p1340(arr: list[int], d: int) -> int:
    """1340. Jump Game V https://leetcode.com/problems/jump-game-v/

    Lessons learned:
    - I solved this using a DFS and DP. The problem structure is

        dp[i] = 1 + max(dp[j] for j in possible_jumps[i])   if possible_jumps[i] is not empty
              = 1                                           else

        possible_jumps[i] = {j: max(i - d, 0) <= j <= min(i + d, n) and arr[j] < arr[i]}

    where n = len(arr). This lends itself well to a recursive DFS solution.

    Examples
    --------
    >>> p1340([6, 4, 14, 6, 8, 13, 9, 7, 10, 6, 12], 2)
    4
    >>> p1340([3, 3, 3, 3, 3], 3)
    1
    >>> p1340([7, 6, 5, 4, 3, 2, 1], 1)
    7

    """
    if len(arr) == 1:
        return 1

    dp = [-1] * len(arr)

    def dfs(i: int):
        if dp[i] > -1:
            return dp[i]

        max_visits = 0
        for i_ in range(i + 1, i + d + 1):
            if not 0 <= i_ < len(arr) or not arr[i] > arr[i_]:
                break
            dfs(i_)
            max_visits = max(max_visits, dp[i_])

        for i_ in range(i - 1, i - d - 1, -1):
            if not 0 <= i_ < len(arr) or not arr[i] > arr[i_]:
                break
            dfs(i_)
            max_visits = max(max_visits, dp[i_])

        dp[i] = 1 + max_visits
        return None

    for i in range(len(arr)):
        dfs(i)

    return max(dp)

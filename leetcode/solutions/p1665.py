def p1665(tasks: list[list[int]]) -> int:
    """1665. Minimum Initial Energy to Finish Tasks https://leetcode.com/problems/minimum-initial-energy-to-finish-tasks/

    You can prove that we should first tackle the tasks with the largest gap
    between min - actual energy. Intuitively, this is because you should tackle
    the high activation energy tasks when you have the most energy. For
    instance, if [[1, 100], [1, 2]], the first task forces at least 100 in the
    bank. A derivable formula is max_k(prefix_actual_k + min_k) where
    prefix_actual_k is the sum of actual energy of the first k - 1 tasks. The
    problem has a fixed total cost, so we need to minimize the peak/max energy.
    With an exchange argument, we can prove the sort order.

    Examples
    --------
    >>> p1665([[1, 2], [2, 4], [4, 8]])
    8
    >>> p1665([[1, 3], [2, 4], [10, 11], [10, 12], [8, 9]])
    32
    >>> p1665([[1, 7], [2, 8], [3, 9], [4, 10], [5, 11], [6, 12]])
    27

    """
    tasks = sorted(tasks, key=lambda x: x[1] - x[0], reverse=True)
    prefix = 0
    energy = tasks[0][1]
    for i in range(len(tasks) - 1):
        prefix += tasks[i][0]
        energy = max(energy, tasks[i + 1][1] + prefix)
    return energy

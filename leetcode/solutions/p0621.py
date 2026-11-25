from collections import Counter


def p621(tasks: list[str], n: int) -> int:
    """621. Task Scheduler https://leetcode.com/problems/task-scheduler

    Lessons learned:
    - This problem can be solved using a greedy approach, where we prioritize
    the most frequent tasks first, to start the cooldown period and fill in the
    other tasks in between.

    Example:
    -------
    Suppose n = 2 and A is the most frequent task, with a frequency F = 4.
    Then our proposed schedule looks like this, where X can be filled in by
    another task

        A X X A X X A X X A

    Note that we have (F - 1) = 3 many periods of length (n + 1) = 3. Now we can
    proceed by filling in the idle spots X with other tasks, making sure to
    spread identical tasks across the periods to meet their cooldown period
    requirement. Since A is the most frequent task, each task can be placed in
    at least one period. If there are more other tasks than idle spots, then we
    can start placing them at the end of each period like so

        A X X B A X X B A X X C A

    So in the case that we have no idle spots remaining, then the time taken is
    just len(tasks). Otherwise, the time taken is the number of periods times
    their length plus the number of elements that share max frequency, that is

        (F - 1) * (n + 1) + #(elements with count F)

    Examples:
    --------
    >>> p621(["A", "A", "A", "B", "B", "B"], 2)
    8
    >>> p621(["A", "C", "A", "B", "D", "B"], 1)
    6
    >>> p621(["A", "A", "A", "B", "B", "B"], 3)
    10
    >>> p621(["A", "A", "B", "B", "C", "C", "D", "D"], 1)
    8
    >>> p621(["A", "A", "B", "B", "C", "C", "D", "D"], 2)
    8
    >>> p621(["A", "A", "B", "B", "C", "C", "D", "D"], 3)
    8
    >>> p621(["A", "A", "B", "B", "C", "C", "D", "D"], 5)
    10
    >>> p621(["A", "A", "A", "B", "B", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K"], 7)
    18

    """
    if n == 0:
        return len(tasks)

    task_counts = Counter(tasks)
    max_count = max(task_counts.values())
    max_count_tasks = sum(1 for count in task_counts.values() if count == max_count)
    return max(
        len(tasks),
        (max_count - 1) * (n + 1) + max_count_tasks,
    )

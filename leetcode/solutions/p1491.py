def p1491(salary: list[int]) -> float:
    """1491. Average Salary Excluding the Minimum and Maximum Salary https://leetcode.com/problems/average-salary-excluding-the-minimum-and-maximum-salary/

    Lessons learned:
    - Slightly surprised the single pass Python-loop approach is slightly faster
    than the three pass approach using built-ins.

    Examples
    --------
    >>> p1491([4000, 3000, 1000, 2000])
    2500.0
    >>> p1491([1000, 2000, 3000])
    2000.0

    """
    return (sum(salary) - min(salary) - max(salary)) / (len(salary) - 2)

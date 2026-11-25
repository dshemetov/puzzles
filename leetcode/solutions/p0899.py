def p899(s: str, k: int) -> str:
    """899. Orderly Queue https://leetcode.com/problems/orderly-queue/

    Lessons learned:
    - This problem is such a troll. At first I thought I found a totally
    ridiculous Copilot suggestion, but then I realized that the solution was
    actually dead simple - you can use the rightmost character as a register and
    rotate the string until the correct insertion point.

    Examples
    --------
    >>> p899("cba", 1)
    'acb'
    >>> p899("baaca", 3)
    'aaabc'
    >>> p899("baaca", 1)
    'aacab'
    >>> p899("baaca", 2)
    'aaabc'
    >>> p899("baaca", 4)
    'aaabc'
    >>> p899("badaca", 2)
    'aaabcd'
    >>> p899("badacadeff", 3)
    'aaabcddeff'

    """
    if k == 1:
        return min(s[i:] + s[:i] for i in range(len(s)))

    return "".join(sorted(s))

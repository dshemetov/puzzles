from collections import deque


def p1404(s: str) -> int:
    """1404. Number of Steps to Reduce a Number in Binary Representation to One
    https://leetcode.com/problems/number-of-steps-to-reduce-a-number-in-binary-representation-to-one

    Examples
    --------
    >>> p1404("1101")
    6
    >>> p1404("10")
    1
    >>> p1404("1")
    0
    >>> p1404("111")
    4

    """
    d = deque(s)
    steps = 0
    while len(d) > 1:
        if d.pop() == "1":
            steps += 1
            i = len(d) - 1
            while i >= 0 and d[i] == "1":
                d[i] = "0"
                i -= 1
            if i == -1:
                d.insert(0, "1")
            else:
                d[i] = "1"
        steps += 1
    return steps

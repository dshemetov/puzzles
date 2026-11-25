from collections import deque


def p649(senate: str) -> str:
    """649. Dota2 Senate https://leetcode.com/problems/dota2-senate/

    Examples
    --------
    >>> p649("RD")
    'Radiant'
    >>> p649("RDD")
    'Dire'
    >>> p649("DDRRR")
    'Dire'
    >>> p649("D")
    'Dire'
    >>> p649("R")
    'Radiant'

    """
    if senate == "":
        return ""

    queue = deque(senate)
    Rcount = queue.count("R")
    Rvetoes, Dvetoes = 0, 0
    while 0 < Rcount < len(queue):
        s = queue.popleft()
        if s == "R":
            if Dvetoes > 0:
                Dvetoes -= 1
                Rcount -= 1
                continue
            Rvetoes += 1
        else:
            if Rvetoes > 0:
                Rvetoes -= 1
                continue
            Dvetoes += 1
        queue.append(s)

    return "Radiant" if queue[0] == "R" else "Dire"

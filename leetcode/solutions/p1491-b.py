import sys


def p1491b(salary: list[int]) -> float:
    """Examples
    >>> p1491b([4000, 3000, 1000, 2000])
    2500.0
    >>> p1491b([1000, 2000, 3000])
    2000.0

    """
    lo, hi = sys.maxsize, -sys.maxsize - 1
    sums = 0
    count = 0
    for s in salary:
        lo = min(s, lo)
        hi = max(s, hi)
        sums += s
        count += 1

    return (sums - lo - hi) / (count - 2)

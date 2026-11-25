def p2485(n: int) -> int:
    """2485. Find the Pivot Integer

    Lessons learned:
    - This one has a cute algebraic solution. Starting with the algebraic
    definition of the point we're looking for i, we have

        i (i + 1) / 2 = n (n + 1) / 2 - i (i + 1) / 2 + i
        i (i + 1) - i = n (n + 1) / 2
        i^2 = n (n + 1) / 2

    So i has a solution iff n (n + 1) / 2 is a perfect square.

    Examples
    --------
    >>> p2485(8)
    6
    >>> p2485(1)
    1
    >>> p2485(4)
    -1

    """
    x = (n * (n + 1) // 2) ** 0.5
    return int(x) if int(x) == x else -1

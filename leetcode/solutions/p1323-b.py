def p1323b(num: int) -> int:
    """Examples
    >>> p1323b(9669)
    9969
    >>> p1323b(9996)
    9999
    >>> p1323b(9999)
    9999

    """
    return int(str(num).replace("6", "9", 1))

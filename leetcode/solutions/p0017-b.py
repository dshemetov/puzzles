def p17b(digits: str) -> list[str]:
    """Examples
    >>> p17b("23")
    ['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf']
    >>> p17b("")
    []
    >>> p17b("2")
    ['a', 'b', 'c']

    """
    if not digits:
        return []

    letter_map = {
        "2": "abc",
        "3": "def",
        "4": "ghi",
        "5": "jkl",
        "6": "mno",
        "7": "pqrs",
        "8": "tuv",
        "9": "wxyz",
    }

    res = []
    for c in digits:
        res = [a + b for a in res for b in letter_map[c]] if res else list(letter_map[c])

    return res

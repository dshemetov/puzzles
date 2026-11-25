from itertools import product


def p17(digits: str) -> list[str]:
    """17. Letter Combinations of a Phone Number https://leetcode.com/problems/letter-combinations-of-a-phone-number/

    Lessons learned:
    - Implement the Cartesian product, they say! It's fun, they say! And it turns
    out, that it is kinda fun.
    - The second solution is a little more manual, but worth knowing.


    Examples
    --------
    >>> p17("23")
    ['ad', 'ae', 'af', 'bd', 'be', 'bf', 'cd', 'ce', 'cf']
    >>> p17("")
    []
    >>> p17("2")
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

    res = product(*[letter_map[c] for c in digits])
    return ["".join(t) for t in res]

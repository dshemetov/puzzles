def p6(s: str, numRows: int) -> str:
    """6. Zigzag Conversion https://leetcode.com/problems/zigzag-conversion/

    Lessons learned:
    - I went directly for figuring out the indexing patterns, since the matrix
    approach seemed too boring. After writing out a few examples for numRows =
    3, 4, 5, I found the pattern.
    - The second solution is a very clever solution from the discussion. It relies
    on the fact that each new character must be appended to one of the rows, so
    it just keeps track of which row to append to.

    Examples
    --------
    >>> p6("PAYPALISHIRING", 1)
    'PAYPALISHIRING'
    >>> p6("PAYPALISHIRING", 2)
    'PYAIHRNAPLSIIG'
    >>> p6("PAYPALISHIRING", 3)
    'PAHNAPLSIIGYIR'
    >>> p6("PAYPALISHIRING", 4)
    'PINALSIGYAHRPI'
    >>> p6("A", 1)
    'A'
    >>> p6("A", 3)
    'A'

    """
    if numRows == 1:
        return s

    if numRows == 2:
        return s[::2] + s[1::2]

    new_s = []
    for i in range(0, numRows):
        if i in {0, numRows - 1}:  # noqa: SIM108
            gaps = [2 * numRows - 2, 2 * numRows - 2]
        else:
            gaps = [2 * numRows - 2 - 2 * i, 2 * i]

        ix, j = i, 0

        while ix < len(s):
            new_s += s[ix]
            ix += gaps[j % 2]
            j += 1

    return "".join(new_s)

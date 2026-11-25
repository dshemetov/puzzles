from array import array


def p151b(s: str) -> str:
    """Examples
    >>> p151b("the sky is blue")
    'blue is sky the'
    >>> p151b("  hello world!  ")
    'world! hello'
    >>> p151b("a good   example")
    'example good a'
    >>> p151b("  Bob    Loves  Alice   ")
    'Alice Loves Bob'

    """
    a = array("u", [])
    a.fromunicode(s.strip())
    a.reverse()

    # Reverse each word
    n = len(a)
    lo = 0
    for i in range(n):
        if a[i] == " ":
            hi = i - 1
            while lo < hi:
                a[lo], a[hi] = a[hi], a[lo]
                lo += 1
                hi -= 1
            lo = i + 1

    hi = n - 1
    while lo < hi:
        a[lo], a[hi] = a[hi], a[lo]
        lo += 1
        hi -= 1

    # Contract spaces in the string
    lo, space = 0, 0
    for i in range(n):
        space = space + 1 if a[i] == " " else 0
        if space <= 1:
            a[lo] = a[i]
            lo += 1

    return "".join(a[:lo])

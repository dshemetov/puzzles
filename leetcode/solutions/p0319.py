def p319(n: int) -> int:
    """319. Bulb Switcher https://leetcode.com/problems/bulb-switcher/

    Lessons learned:
    - Testing the array at n=50, I saw that only square numbers remained. From
    there it was easy to prove that square numbers are the only ones with an odd
    number of factors. So this problem is just counting the number of perfect
    squares <= n.

    Examples
    --------
    >>> p319(3)
    1
    >>> p319(0)
    0
    >>> p319(1)
    1
    >>> p319(5)
    2

    """
    arr = [0] * n
    for i in range(1, n + 1):
        for j in range(0, n):
            if (j + 1) % i == 0:
                arr[j] = 1 if arr[j] == 0 else 0
    return sum(arr)

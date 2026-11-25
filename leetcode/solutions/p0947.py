from collections import defaultdict


def p947(stones: list[list[int]]) -> int:
    """947. Most Stones Removed With Same Row or Column https://leetcode.com/problems/most-stones-removed-with-same-row-or-column/

    Lessons learned:
    - The key idea is that we can remove all stones in each connected component
    except one. We can use dfs to find the connected components. Fun fact: the
    dfs can avoid recursion by using a stack.

    Examples
    --------
    >>> p947([[0, 0], [0, 1], [1, 0], [1, 2], [2, 1], [2, 2]])
    5
    >>> p947([[0, 0], [0, 2], [1, 1], [2, 0], [2, 2]])
    3
    >>> p947([[0, 0]])
    0
    >>> p947([[0, 0], [0, 1], [1, 1]])
    2
    >>> p947([[0, 1], [1, 0]])
    0

    """
    rows = defaultdict(list)
    cols = defaultdict(list)

    for i, (r, c) in enumerate(stones):
        rows[r].append(i)
        cols[c].append(i)

    seen = set()

    def dfs(i: int) -> None:
        """Dfs without recursion"""
        stack = [i]
        while stack:
            j = stack.pop()
            seen.add(j)
            stack.extend(k for k in rows[stones[j][0]] + cols[stones[j][1]] if k not in seen)

    n_components = 0
    for i in range(len(stones)):
        if i not in seen:
            dfs(i)
            n_components += 1

    return len(stones) - n_components

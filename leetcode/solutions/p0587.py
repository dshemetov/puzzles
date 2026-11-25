# /// script
# requires-python = ">=3.14"
# dependencies = ["numpy"]
# ///
import math
from collections import defaultdict
from collections.abc import Callable
from fractions import Fraction
from typing import Optional, cast

import numpy as np


class ListNode:
    def __init__(self, val: int = 0, next: Optional["ListNode"] = None):  # noqa: A002 pylint: disable=redefined-builtin
        self.val = val
        self.next = next

    @staticmethod
    def from_list(lst: list[int]) -> Optional["ListNode"]:
        if not lst:
            return None

        original_head = head = ListNode(lst[0])
        for x in lst[1:]:
            head.next = ListNode(x)
            head = head.next

        return original_head

    @staticmethod
    def from_int(i: int) -> "ListNode":
        num_list = None
        for x in str(i):
            num_list = ListNode(val=int(x), next=num_list)
        return cast(ListNode, num_list)


def list_to_int(lst: ListNode | None) -> int:
    """Examples
    >>> list_to_int(ListNode.from_int(0))
    0
    >>> list_to_int(ListNode.from_int(2))
    2
    >>> list_to_int(ListNode.from_int(12))
    12
    >>> list_to_int(ListNode.from_int(15))
    15
    >>> list_to_int(ListNode.from_int(255))
    255
    """
    num = 0
    digit = 0
    while lst:
        num += lst.val * 10**digit
        digit += 1
        lst = lst.next
    return num


def ccw(p1: tuple[int, int], p2: tuple[int, int], p3: tuple[int, int]) -> float:
    """Examples
    >>> ccw((0, 0), (1, 0), (0, 1))
    1.0
    >>> ccw((0, 0), (1, 0), (1, 1))
    1.0
    >>> ccw((0, 0), (1, 0), (1, 0))
    0.0
    >>> ccw((0, 0), (1, 0), (0, -1))
    -1.0

    """
    v1 = (p2[0] - p1[0], p2[1] - p1[1])
    v2 = (p3[0] - p2[0], p3[1] - p2[1])
    return float(v1[0] * v2[1] - v1[1] * v2[0])


def atan2notan(y: int, x: int) -> tuple[int, int | Fraction]:
    """A polar angle substitute without trigonometry or floating points.

    Imagine tracing out a circle counterclockwise and measuring the angle to the tracing vector
    from the positive x axis. This is the sorted order we wish to achieve. This function will give
    a lexically smaller tuple for smaller angles.
    """
    if x == 0 and y == 0:
        return (0, 0)
    if x > 0 and y >= 0:
        return (0, Fraction(y, x))
    if x == 0 and y > 0:
        return (1, 0)
    if x < 0:
        return (2, Fraction(y, x))
    if x == 0 and y < 0:
        return (3, 0)
    if y < 0 < x:
        return (4, Fraction(y, x))
    raise ValueError("How did you even get here?")


def partition_by(lst: list, f: Callable) -> dict:
    """Partition a list into lists based on a predicate."""
    d = defaultdict(list)
    for item in lst:
        d[f(item)].append(item)
    return d


def p1(nums: list[int], target: int) -> list[int]:
    """1. Two Sum https://leetcode.com/problems/two-sum/

    Examples
    --------
    >>> p1([3, 3], 6)
    [0, 1]
    >>> p1([3, 2, 4], 7)
    [0, 2]

    """
    ix_map = defaultdict(list)
    for i, x in enumerate(nums):
        ix_map[x].append(i)

    for x in ix_map:
        if ix_map.get(target - x):
            if x == target - x and len(ix_map[x]) == 2:
                return ix_map[target - x]
            if x != target - x:
                return [ix_map[x][0], ix_map[target - x][0]]
    return []


def p2(l1: ListNode | None, l2: ListNode | None) -> ListNode | None:
    """2. Add Two Numbers https://leetcode.com/problems/add-two-numbers/

    Examples
    --------
    >>> list_to_int(p2(ListNode.from_int(0), ListNode.from_int(15)))
    15
    >>> list_to_int(p2(ListNode.from_int(12), ListNode.from_int(15)))
    27
    >>> list_to_int(p2(ListNode.from_int(12), ListNode.from_int(153)))
    165

    """
    first_node = ListNode(0)
    cur_node = first_node
    carry_bit = 0
    while l1 or l2 or carry_bit > 0:
        x = l1.val if l1 else 0
        y = l2.val if l2 else 0

        num = x + y + carry_bit
        carry_bit = num // 10

        new_node = ListNode(num % 10)
        cur_node.next = new_node
        cur_node = new_node

        l1 = l1.next if l1 else None
        l2 = l2.next if l2 else None

    return first_node.next


def p3(s: str) -> int:
    """3. Longest Substring Without Repeating Characters https://leetcode.com/problems/longest-substring-without-repeating-characters/

    Examples
    --------
    >>> p3("a")
    1
    >>> p3("aa")
    1
    >>> p3("aaa")
    1
    >>> p3("aab")
    2
    >>> p3("abba")
    2
    >>> p3("abccba")
    3
    >>> p3("au")
    2
    >>> p3("cdd")
    2
    >>> p3("abcabcbb")
    3
    >>> p3("aabcdef")
    6
    >>> p3("abcdeffff")
    6
    >>> p3("dvdf")
    3
    >>> p3("ohomm")
    3

    """
    if not s:
        return 0

    longest = 1
    lo = 0
    hi = 1
    char_set = set(s[lo])
    while hi < len(s):
        if s[hi] not in char_set:
            char_set.add(s[hi])
            hi += 1
            longest = max(longest, hi - lo)
        else:
            char_set.remove(s[lo])
            lo += 1

    return longest


def p587(trees: list[list[int]]) -> list[list[int]]:
    """587. Erect the Fence https://leetcode.com/problems/erect-the-fence/

    Lessons learned:
    - A broad class of computational geometry algorithms solve this:
    https://en.wikipedia.org/wiki/Convex_hull_algorithms#Algorithms
    - The Graham scan is easy to understand and decently fast:
    https://en.wikipedia.org/wiki/Graham_scan
    - Tip from a graphics guy: avoid representing angles with degrees/radians,
    stay in fractions. This avoids numerical issues with floating points, but
    it's not without its own problems.
    - The atan2 function was invented back in the Fortran days and makes for a
    stable polar angle definition. It's also fast.
    - The edge-cases of the Graham scan are tricky, especially all the cases with
    colinear points.

    Examples
    --------
    >>> p587([[1, 1], [2, 2], [2, 0], [2, 4], [3, 3], [4, 2]])
    [[2, 0], [4, 2], [3, 3], [2, 4], [1, 1]]
    >>> p587([[1, 2], [2, 2], [4, 2]])
    [[1, 2], [2, 2], [4, 2]]
    >>> p587([[1, 1], [2, 2], [3, 3], [2, 1], [4, 1], [2, 3], [1, 3]])
    [[1, 1], [2, 1], [4, 1], [3, 3], [2, 3], [1, 3]]
    >>> p587(
    ...     [
    ...         [3, 0],
    ...         [4, 0],
    ...         [5, 0],
    ...         [6, 1],
    ...         [7, 2],
    ...         [7, 3],
    ...         [7, 4],
    ...         [6, 5],
    ...         [5, 5],
    ...         [4, 5],
    ...         [3, 5],
    ...         [2, 5],
    ...         [1, 4],
    ...         [1, 3],
    ...         [1, 2],
    ...         [2, 1],
    ...         [4, 2],
    ...         [0, 3],
    ...     ]
    ... )
    [[3, 0], [4, 0], [5, 0], [6, 1], [7, 2], [7, 3], [7, 4], [6, 5], [5, 5], [4, 5], [3, 5], [2, 5], [1, 4], [0, 3], [1, 2], [2, 1]]
    >>> p587([[0, 2], [0, 1], [0, 0], [1, 0], [2, 0], [1, 1]])
    [[0, 0], [1, 0], [2, 0], [1, 1], [0, 2], [0, 1]]
    >>> p587(
    ...     [
    ...         [0, 2],
    ...         [0, 4],
    ...         [0, 5],
    ...         [0, 9],
    ...         [2, 1],
    ...         [2, 2],
    ...         [2, 3],
    ...         [2, 5],
    ...         [3, 1],
    ...         [3, 2],
    ...         [3, 6],
    ...         [3, 9],
    ...         [4, 2],
    ...         [4, 5],
    ...         [5, 8],
    ...         [5, 9],
    ...         [6, 3],
    ...         [7, 9],
    ...         [8, 1],
    ...         [8, 2],
    ...         [8, 5],
    ...         [8, 7],
    ...         [9, 0],
    ...         [9, 1],
    ...         [9, 6],
    ...     ]
    ... )
    [[9, 0], [9, 1], [9, 6], [7, 9], [5, 9], [3, 9], [0, 9], [0, 5], [0, 4], [0, 2], [2, 1]]
    >>> p587([[0, 0], [0, 1], [0, 2], [1, 2], [2, 2], [3, 2], [3, 1], [3, 0], [2, 0], [1, 0], [1, 1], [3, 3]])
    [[0, 0], [1, 0], [2, 0], [3, 0], [3, 1], [3, 2], [3, 3], [0, 2], [0, 1]]

    """
    lowest_left_point = (math.inf, math.inf)
    for x, y in trees:
        if y < lowest_left_point[1] or (y == lowest_left_point[1] and x < lowest_left_point[0]):
            lowest_left_point = (x, y)

    trees_by_slope = partition_by(
        trees,
        lambda p: atan2notan(p[1] - lowest_left_point[1], p[0] - lowest_left_point[0]),
    )
    slopes = sorted(trees_by_slope.keys())

    # Handles many colinear cases; order doesn't matter for leetcode
    if len(slopes) == 1:
        return trees

    def distance(p1, p2):
        return np.linalg.norm((p1[1] - p2[1], p1[0] - p2[0]))

    # The right-most line should sort by increasing distance from lowest left point
    trees_by_slope[slopes[0]] = sorted(trees_by_slope[slopes[0]], key=lambda p: distance(p, lowest_left_point))
    # The left-most line should sort by decreasing distance from lowest left point
    trees_by_slope[slopes[-1]] = sorted(trees_by_slope[slopes[-1]], key=lambda p: -distance(p, lowest_left_point))
    # The rest should sort by increasing distance from lowest left point
    for slope in slopes[1:-1]:
        trees_by_slope[slope] = sorted(trees_by_slope[slope], key=lambda p: distance(p, lowest_left_point))

    stack = []
    for slope in slopes:
        for tree in trees_by_slope[slope]:
            while len(stack) >= 2 and ccw(stack[-2], stack[-1], tree) < 0:
                stack.pop()
            stack.append(tree)

    return stack


if __name__ == "__main__":
    import doctest

    doctest.testmod()

import sys
from typing import Optional, cast


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


def listnode_to_list(head) -> list[int]:
    """Examples
    >>> listnode_to_list(ListNode.from_list([1, 2, 3, 4, 5]))
    [1, 2, 3, 4, 5]
    """
    lst = []
    ptr = head
    while ptr:
        lst.append(ptr.val)
        ptr = ptr.next

    return lst


def p23(lists: list[ListNode | None]) -> ListNode | None:
    """23. Merge k Sorted Lists https://leetcode.com/problems/merge-k-sorted-lists/

    Lessons learned:
    - Sometimes the hard problems aren't that hard.

    Examples
    --------
    >>> listnode_to_list(
    ...     p23([ListNode.from_list([1, 4, 5]), ListNode.from_list([1, 3, 4]), ListNode.from_list([2, 6])])
    ... )
    [1, 1, 2, 3, 4, 4, 5, 6]
    >>> listnode_to_list(p23([]))
    []
    >>> listnode_to_list(p23([None]))
    []

    """
    head = pointer = ListNode()

    while any(x for x in lists):
        min_val = sys.maxsize
        min_idx = -1
        for i, x in enumerate(lists):
            if x and x.val < min_val:
                min_val = x.val
                min_idx = i

        pointer.next = lists[min_idx]
        lists[min_idx] = lists[min_idx].next
        pointer = pointer.next

    return head.next

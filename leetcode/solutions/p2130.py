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


def p2130(head: ListNode | None) -> int:
    """2130. Maximum Twin Sum of a Linked List https://leetcode.com/problems/maximum-twin-sum-of-a-linked-list/

    Lessons learned:
    - Finding the midpoint of a linked list can be done with two pointers.
    Reversing a linked list is pretty easy. These steps above can be done in one
    pass.

    Examples
    --------
    >>> p2130(ListNode.from_list([5, 4, 2, 1]))
    6
    >>> p2130(ListNode.from_list([4, 2, 2, 3]))
    7
    >>> p2130(ListNode.from_list([1, 100000]))
    100001

    """
    if head is None:
        return 0

    # Find the midpoint
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next

    # Reverse the second half
    prev = None
    while slow:
        slow.next, prev, slow = prev, slow, slow.next

    # Find the maximum sum
    m = 0
    while prev:
        m = max(m, prev.val + head.val)
        prev = prev.next
        head = head.next

    return m

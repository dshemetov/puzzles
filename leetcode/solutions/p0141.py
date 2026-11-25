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


def p141(head: ListNode | None) -> bool:
    """141. Linked List Cycle https://leetcode.com/problems/linked-list-cycle/

    Lessons learned:
    - We use the classic two-pointer cycle detection algorithm known as Floyd's
    Tortoise and Hare.
    - One intuitive way to think about why this works is to imagine the tortoise
    as ahead of the hare once it enters the cycle section. Then, the hare gets
    closer to the tortoise with each step and eventually it will catch up, since
    their relative speed difference is 1.
    - An algebraic proof: we want to show that

        i  = n + m
        2i = n + k * p + m
        ------------------
        n + m = k * p

    has a solution in k >= 0 and m >= 0, where n is the number of nodes before
    the cycle, p is the number of nodes in the cycle, and m is the number of
    nodes in the cycle before the hare catches up to the tortoise. Setting k = n
    and m = n * p - n, we have a solution. For instance, if n = 5 and p = 3,
    this gives the solution k = 5 and m = 10, which translates to i = 15 and 2i
    = 30, which works in the table below:

        Tortoise index: 0, 1, 2, 3, 4,  5,  6,  7,  8,  9, 10, 11, 12, 13, 14, 15, ...
        Tortoise node:  1, 2, 3, 4, 5,  6,  7,  5,  6,  7,  5,  6,  7,  5,  6,  7, ...
        Hare index:     0, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, ...
        Hare node:      1, 3, 5, 7, 5,  7,  5,  7,  5,  7,  5,  7,  5,  7,  5,  7, ...

    This is not the earliest solution, but it is an existence proof.
    """
    slow = fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
        if slow == fast:
            return True
    return False

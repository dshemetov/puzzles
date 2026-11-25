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


def p876(head: ListNode | None) -> ListNode | None:
    """876. Middle of the Linked List https://leetcode.com/problems/middle-of-the-linked-list

    Examples
    --------
    >>> listnode_to_list(p876(ListNode.from_list([1, 2, 3, 4, 5])))
    [3, 4, 5]
    >>> listnode_to_list(p876(ListNode.from_list([1, 2, 3, 4, 5, 6])))
    [4, 5, 6]

    """
    if not head or not head.next:
        return head
    slow = head
    fast = head
    while fast and fast.next:
        slow = slow.next
        fast = fast.next.next
    return slow

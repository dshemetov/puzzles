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


def p21(list1: ListNode | None, list2: ListNode | None) -> ListNode | None:
    """21. Merge Two Sorted Lists https://leetcode.com/problems/merge-two-sorted-lists/

    Examples
    --------
    >>> listnode_to_list(p21(ListNode.from_list([1, 2, 4]), ListNode.from_list([1, 3, 4])))
    [1, 1, 2, 3, 4, 4]
    >>> listnode_to_list(p21(None, None))
    []
    >>> listnode_to_list(p21(None, ListNode.from_list([0])))
    [0]

    """
    head = pointer = ListNode()

    while list1 and list2:
        if list1.val < list2.val:
            pointer.next = list1
            list1 = list1.next
        else:
            pointer.next = list2
            list2 = list2.next
        pointer = pointer.next

    if list1:
        pointer.next = list1

    if list2:
        pointer.next = list2

    return head.next


def p23b(lists: list[ListNode | None]) -> ListNode | None:
    """Examples
    >>> listnode_to_list(
    ...     p23b([ListNode.from_list([1, 4, 5]), ListNode.from_list([1, 3, 4]), ListNode.from_list([2, 6])])
    ... )
    [1, 1, 2, 3, 4, 4, 5, 6]
    >>> listnode_to_list(p23b([]))
    []
    >>> listnode_to_list(p23b([None]))
    []

    """
    if not lists:
        return None

    while len(lists) > 1:
        lists.append(p21(lists.pop(0), lists.pop(0)))

    return lists[0]

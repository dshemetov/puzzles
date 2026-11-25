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


def p24(head: ListNode | None) -> ListNode | None:
    """24. Swap Nodes in Pairs https://leetcode.com/problems/swap-nodes-in-pairs/

    Examples
    --------
    >>> listnode_to_list(p24(None))
    []
    >>> listnode_to_list(p24(ListNode.from_list([1])))
    [1]
    >>> listnode_to_list(p24(ListNode.from_list([1, 2])))
    [2, 1]
    >>> listnode_to_list(p24(ListNode.from_list([1, 2, 3])))
    [2, 1, 3]
    >>> listnode_to_list(p24(ListNode.from_list([1, 2, 3, 4])))
    [2, 1, 4, 3]
    >>> listnode_to_list(p24(ListNode.from_list([1, 2, 3, 4, 5])))
    [2, 1, 4, 3, 5]

    """
    if not head:
        return None
    if not head.next:
        return head

    pointer = head
    new_head = head.next

    # 1 2 3 4
    # 2 1 4 3
    while pointer and pointer.next:
        one = pointer
        two = pointer.next
        three = pointer.next.next
        four = pointer.next.next.next if three else None

        one.next = four if four else three
        two.next = one

        pointer = three

    return new_head

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

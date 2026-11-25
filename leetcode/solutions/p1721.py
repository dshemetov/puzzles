from collections import defaultdict
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


def p1721(head: ListNode, k: int) -> ListNode:
    """1721. Swapping Nodes in a Linked List https://leetcode.com/problems/swapping-nodes-in-a-linked-list/

    Lessons learned:
    - Two pointers allows you to do this in one pass.

    Examples
    --------
    >>> listnode_to_list(p1721(ListNode.from_list([1, 2, 3, 4, 5]), 2))
    [1, 4, 3, 2, 5]
    >>> listnode_to_list(p1721(ListNode.from_list([7, 9, 6, 6, 7, 8, 3, 0, 9, 5]), 5))
    [7, 9, 6, 6, 8, 7, 3, 0, 9, 5]

    """
    p1 = head
    for _ in range(k - 1):
        p1 = p1.next
    node1 = p1
    p2 = head
    while p1.next:
        p1 = p1.next
        p2 = p2.next
    node2 = p2
    node1.val, node2.val = node2.val, node1.val
    return head

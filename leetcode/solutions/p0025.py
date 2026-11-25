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


def p25(head: ListNode | None, k: int) -> ListNode | None:
    """25. Reverse Nodes in k-Group https://leetcode.com/problems/reverse-nodes-in-k-group/description/

    Lessons learned:
    - Walking through the k=3 case below while writing the algorithm was key.
    - Variable naming is hard. It's nice to start with long descriptive names to
    clarify each variable's intent, but then erase them with shorter ones, once
    you're used to it. Short names make thinking easier for some reason, but are
    harder to read.

    Example with k = 3:

    First iteration, after lookahead:

    [1, 2, 3, 4, 5, 6, 7]
     ^head
     ^new_head
     ^cur1
              ^cur2

    After reversal:

    [1, 2, 3, 4, 5, 6, 7]
     ^head
     ^first_prev
     ^first_cur
           ^new_head
              ^cur1
              ^cur2

    Second iteration, after lookahead:

    [1, 2, 3, 4, 5, 6, 7]
     ^head
     ^first_prev
           ^new_head
              ^cur1
                       ^cur2

    After reversal:

    [1, 2, 3, 4, 5, 6, 7]
     ^head
             ^first_prev
           ^new_head
              ^first_cur
                       ^cur1
                       ^cur2

    >>> listnode_to_list(p25(ListNode.from_list([1, 2, 3, 4, 5]), 2))
    [2, 1, 4, 3, 5]
    >>> listnode_to_list(p25(ListNode.from_list([1, 2, 3, 4, 5]), 3))
    [3, 2, 1, 4, 5]
    >>> listnode_to_list(p25(ListNode.from_list([1, 2, 3, 4, 5]), 1))
    [1, 2, 3, 4, 5]
    """
    # Start of new list
    new_head = head
    # Reversal pointer
    cur1 = head
    # Lookahead pointer
    cur2 = head
    # Pointer for linking two reversed segments together (e.g. 1 2 3 4 with k =
    # 2, it stores 1 so we can link it to 4)
    first_prev = None
    first_reversal = True

    while True:
        # Look ahead
        i = 0
        while i < k and cur2:
            cur2 = cur2.next
            i += 1

        if i < k:
            return new_head

        # Reverse section, see p2130
        first_cur = cur1
        i = 0
        cur1_prev = None
        while cur1 and i < k:
            cur1.next, cur1_prev, cur1 = cur1_prev, cur1, cur1.next
            i += 1

        # If first reversal, update the new_head
        if first_reversal:
            new_head = cur1_prev
            first_reversal = False
        else:
            first_prev.next = cur1_prev
        first_prev = first_cur
        first_cur.next = cur1

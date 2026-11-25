from collections import deque
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


class Node:
    def __init__(self, val: int = 0, neighbors: list["Node"] | None = None):
        self.val = val
        self.neighbors = neighbors if neighbors is not None else []

    @staticmethod
    def from_adjacency_list(adjacency_list: list[list[int]]) -> "Node":
        """Build a node-based graph from an adjacency list.

        Examples
        --------
        >>> Node.from_adjacency_list([[1, 2], [1, 4], [2, 3], [3, 4]]).to_adjacency_list()
        [[1, 2], [1, 4], [2, 3], [3, 4]]

        """
        if adjacency_list == [[]]:
            return Node(1)

        node_index = {}
        for x, y in adjacency_list:
            if (xnode := node_index.get(x)) is None:
                xnode = Node(x)
                node_index[x] = xnode
            if (ynode := node_index.get(y)) is None:
                ynode = Node(y)
                node_index[y] = ynode

            xnode.neighbors.append(ynode)
            ynode.neighbors.append(xnode)

        return node_index[1]

    def to_adjacency_list(self) -> list[list[int]]:
        """Traverse through a graph and build an adjacency list."""
        adjacency_list = set()
        visited = set()
        node_queue: deque[Node] = deque([self])

        while node_queue:
            node = node_queue.popleft()
            visited.add(node.val)

            for neighbor in node.neighbors:
                adjacency_list.add(tuple(sorted([node.val, neighbor.val])))

                if neighbor.val not in visited:
                    node_queue.append(neighbor)

        return sorted([list(e) for e in adjacency_list], key=lambda x: (x[0], x[1]))


def p19(head: ListNode | None, n: int) -> ListNode | None:
    """19. Remove Nth Node From End of List https://leetcode.com/problems/remove-nth-node-from-end-of-list/

    Examples
    --------
    >>> listnode_to_list(p19(ListNode.from_list([1, 2, 3, 4, 5]), 1))
    [1, 2, 3, 4]
    >>> listnode_to_list(p19(ListNode.from_list([1, 2, 3, 4, 5]), 2))
    [1, 2, 3, 5]
    >>> listnode_to_list(p19(ListNode.from_list([1, 2, 3, 4, 5]), 3))
    [1, 2, 4, 5]
    >>> listnode_to_list(p19(ListNode.from_list([1, 2, 3, 4, 5]), 4))
    [1, 3, 4, 5]
    >>> listnode_to_list(p19(ListNode.from_list([1, 2, 3, 4, 5]), 5))
    [2, 3, 4, 5]
    >>> listnode_to_list(p19(ListNode.from_list([1]), 1))
    []
    >>> listnode_to_list(p19(ListNode.from_list([1, 2]), 1))
    [1]
    >>> listnode_to_list(p19(ListNode.from_list([1, 2]), 2))
    [2]

    """
    if not head:
        return None

    sz = 0
    node = head
    while node:
        node = node.next
        sz += 1

    if sz == 1:
        return None

    if sz == n:
        return head.next

    node = head
    for _ in range(sz - n - 1):
        node = node.next

    node.next = node.next.next

    return head

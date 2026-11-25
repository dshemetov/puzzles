import math
from typing import Optional


class TreeNode:
    def __init__(
        self,
        val: int = 0,
        left: Optional["TreeNode"] = None,
        right: Optional["TreeNode"] = None,
    ):
        self.val = val
        self.left = left
        self.right = right

    @staticmethod
    def from_list(lst: list, recursive: bool = False) -> "TreeNode":
        """Build TreeNode from a top-to-bottom, left-to-right traversal of the nodes.

        With a 0-indexed array, a node at index i has left and right children at
        index 2i+1 and 2i+2.
        """
        if recursive:
            # Must be length 2 ** i - 1.
            assert math.log2(len(lst) + 1) == int(math.log2(len(lst) + 1))
            tree_depth = math.floor(math.log2(len(lst)))

            if len(lst) == 1:
                return TreeNode(lst[0])

            if len(lst) == 3:
                return TreeNode(
                    lst[0],
                    TreeNode(lst[1]) if lst[1] is not None else None,
                    TreeNode(lst[2]) if lst[2] is not None else None,
                )

            left_lst = []
            right_lst = []

            for i in range(1, tree_depth + 1):
                left_lst.extend(lst[2**i - 1 : 2**i - 1 + 2 ** (i - 1)])
                right_lst.extend(lst[2**i - 1 + 2 ** (i - 1) : 2 ** (i + 1) - 1])

            return TreeNode(
                lst[0],
                TreeNode.from_list(left_lst, recursive=True),
                TreeNode.from_list(right_lst, recursive=True),
            )

        root = TreeNode(lst[0])
        queue = [root]
        i = 1
        while i < len(lst):
            node = queue.pop(0)
            if lst[i] is not None:
                node.left = TreeNode(lst[i])
                queue.append(node.left)
            i += 1
            if i < len(lst) and lst[i] is not None:
                node.right = TreeNode(lst[i])
                queue.append(node.right)
            i += 1
        return root


def p222(root: TreeNode | None) -> int:
    """222. Count Complete Tree Nodes https://leetcode.com/problems/count-complete-tree-nodes/

    Lessons learned:
    - A complete binary tree is a binary tree in which every level is completely
    filled, except for the last where the nodes must be as far left as possible.

    Examples
    --------
    >>> p222(TreeNode.from_list([1, 2, 3, 4, 5, 6]))
    6
    >>> p222(TreeNode.from_list([1, 2, 3, 4, 5, 6, None]))
    6
    >>> p222(TreeNode.from_list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15]))
    15
    >>> p222(TreeNode.from_list([1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, None, None, None]))
    12

    """
    if not root:
        return 0

    height = -1
    node = root
    while node:
        height += 1
        node = node.left

    if height == 0:
        return 1

    def is_node_in_tree(root: TreeNode, i: int) -> bool:
        node = root
        for c in format(i, f"0{height}b"):
            node = node.left if c == "0" else node.right
        return bool(node)

    lo, hi = 0, int(2 ** (height) - 1)
    while lo <= hi:
        mid = (lo + hi) // 2
        node_in_tree = is_node_in_tree(root, mid)
        if node_in_tree:
            lo = mid + 1
        else:
            hi = mid - 1

    return int(2 ** (height)) + lo - 1

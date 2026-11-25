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


def p102(root: TreeNode | None) -> list[list[int]]:
    """102. Binary Tree Level Order Traversal https://leetcode.com/problems/binary-tree-level-order-traversal/

    Examples
    --------
    >>> p102(TreeNode.from_list([3, 9, 20, None, None, 15, 7]))
    [[3], [9, 20], [15, 7]]
    >>> p102(TreeNode(1))
    [[1]]
    >>> p102(None)
    []

    """
    if not root:
        return []

    queue = [root]
    result = []
    while queue:
        level = []
        new_queue = []
        for x in queue:
            level.append(x.val)
            if x.left:
                new_queue.append(x.left)
            if x.right:
                new_queue.append(x.right)
        result.append(level)
        queue = new_queue
    return result

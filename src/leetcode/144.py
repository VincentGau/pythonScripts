# Definition for a binary tree node.
from collections import deque
from typing import List


class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def gen_tree(values):
    '''
    返回列表对应的二叉树
    :param values:
    :return:
    '''
    if not values:
        return None
    root = TreeNode(values[0])
    queue = deque([root])
    leng = len(values)
    nums = 1
    while nums < leng:
        node = queue.popleft()
        if node:
            node.left = TreeNode(values[nums]) if values[nums] else None
            queue.append(node.left)
            if nums + 1 < leng:
                node.right = TreeNode(values[nums + 1]) if values[nums + 1] else None
                queue.append(node.right)
                nums += 1
            nums += 1
    return root


class Solution:
    def __init__(self):
        self.ret = []

    def preorderTraversal(self, root: TreeNode) -> List[int]:
        if root != None:
            self.ret.append(root.val)
            self.preorderTraversal(root.left)
            self.preorderTraversal(root.right)
        return self.ret


s = Solution()
r = gen_tree([1, 2, 3, 4, None, 5, 6, None, None, None, None, 7])
print(s.preorderTraversal(r))
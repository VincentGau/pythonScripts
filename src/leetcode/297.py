# Definition for a binary tree node.
from collections import deque


class TreeNode(object):
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None

class Codec:
    '''
    二叉树的序列化和反序列化
    '''
    def serialize(self, root):
        """Encodes a tree to a single string.

        :type root: TreeNode
        :rtype: str
        """
        if not root:
            return '[]'
        queue = deque([root])
        res = []
        while queue:
            top = queue.popleft()
            if top:
                res.append(top.val)
                if top.left:
                    queue.append(top.left)
                else:
                    queue.append(None)
                if top.right:
                    queue.append(top.right)
                else:
                    queue.append(None)
            else:
                res.append('null')

        a = 0
        for i in range(len(res) - 1, -1, -1):
            if res[i] != 'null':
                break
            a += 1
        rres = res[:-a]
        return '[' + ','.join('%s' %id for id in rres) + ']'

    def deserialize(self, data):
        """Decodes your encoded data to tree.

        :type data: str
        :rtype: TreeNode
        """
        if data == '[]':
            return None

        l = data[1:-1].split(',')

        root = TreeNode(l[0])
        queue = deque([root])
        i = 1
        while i < len(l):
            node = queue.popleft()
            if node:
                node.left = TreeNode(l[i]) if l[i] != 'null' else None
                queue.append(node.left)
                if i + 1 < len(l):
                    node.right = TreeNode(l[i + 1]) if l[i + 1] != 'null' else None
                    queue.append(node.right)
                    i += 1
                i += 1
        return root


# Your Codec object will be instantiated and called as such:
codec = Codec()
# codec.deserialize(codec.serialize(root))
print(codec.deserialize("[]"))
r = codec.deserialize("[1,2,3,null,null,4,5]")
print(codec.serialize(r))
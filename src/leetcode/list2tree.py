from collections import deque

class TreeNode:
    def __init__(self, x):
        self.val = x
        self.left = None
        self.right = None


def gen_tree(values):
    '''
    根据列表生成二叉树
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


if __name__ == '__main__':
    gen_tree([1, None, 2, 3])
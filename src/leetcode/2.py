# Definition for singly-linked list.
from typing import List


class ListNode:
    def __init__(self, x):
        self.val = x
        self.next = None


def list_to_linkedlist(l: List) -> ListNode:
    if not l:
        return None
    head = ListNode(l[0])
    node = head
    for i in range(1, len(l)):
        node.next = ListNode(l[i])
        node = node.next
    return head


class Solution:
    def addTwoNumbers(self, l1: ListNode, l2: ListNode) -> ListNode:
        if not l1:
            return l2
        if not l2:
            return l1
        p, q = l1, l2
        dummy = ListNode(0)
        cur = dummy
        carry = 0
        while p or q:
            x = p.val if p else 0
            y = q.val if q else 0
            sum = x + y + carry
            carry = sum // 10
            cur.next = ListNode(sum % 10)
            cur = cur.next
            if p:
                p = p.next
            if q:
                q = q.next

        if carry:
            cur.next = ListNode(1)
        return dummy.next



l1 = list_to_linkedlist([2, 4, 3])
l2 = list_to_linkedlist([5, 6, 4])
s = Solution()
s.addTwoNumbers(l1, l2)
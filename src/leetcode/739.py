from typing import List


class Solution:
    def dailyTemperatures(self, T: List[int]) -> List[int]:
        stack = []
        res = [0 for _ in range(len(T))]
        for i in range(len(T)):
            while stack and T[i] > T[stack[-1]]:
                top = stack[-1]
                res[top] = i - top
                stack.pop()
            stack.append(i)
        return res

s = Solution()
print(s.dailyTemperatures([73, 74, 75, 71, 69, 72, 76, 73]))
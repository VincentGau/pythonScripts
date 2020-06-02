from typing import List


class Solution:
    def largestRectangleArea(self, heights: List[int]) -> int:
        temp_heights = [-1] + heights + [-1]
        left = [0] * (len(heights) + 1)
        right = [0] * (len(heights) + 1)
        max_area = 0

        for i in range(1, len(heights) + 1):
            cur = i
            while temp_heights[i] <= temp_heights[cur - 1]:
                cur = left[cur - 1]
            left[i] = cur

        for i in range(len(heights), 0, -1):
            cur = i
            while temp_heights[i] <= temp_heights[cur + 1]:
                cur = right[cur + 1]
            right[i] = cur

        for i in range(1, len(heights) + 1):
            max_area = max(max_area, temp_heights[i] * (right[i] - left[i] + 1))

        return max_area


s = Solution()
print(s.largestRectangleArea([2, 1, 5, 6, 2, 3]))
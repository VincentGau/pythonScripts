from typing import List


class Solution:
    def findBestValue(self, arr: List[int], target: int) -> int:
        left, right = 0, 0
        for num in arr:
            right = max(right, num)

        while left < right:
            mid = left + (right - left) // 2
            sum = self.custom_sum(arr, mid)
            if sum < target:
                left = mid + 1
            else:
                right = mid

        sum1 = self.custom_sum(arr, left - 1)
        sum2 = self.custom_sum(arr, left)
        if target - sum1 <= sum2 - target:
            return left - 1
        return left

    def custom_sum(self, arr, num):
        sum = 0
        for a in arr:
            sum += min(a, num)
        return sum


s = Solution()
print(s.findBestValue([2, 3, 5],10))

from typing import List


class Solution:
    def canPartition(self, nums: List[int]) -> bool:
        if sum(nums) % 2:
            return False
        half = sum(nums) // 2

        dp = [0 for _ in range(sum(nums) + 1)]
        dp[0] = 1

        for num in nums:
            for i in range(sum(nums) // 2, -1, -1):
                if dp[i]:
                    dp[i + num] = 1
            if dp[half]:
                return True
        return False


s = Solution()
print(s.canPartition([1, 5, 11, 5]))
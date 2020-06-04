from typing import List


class Solution:
    def change(self, amount: int, coins: List[int]) -> int:
        dp = [1 for _ in range(amount)]
        for coin in coins:
            for j in range(1, amount):
                if j >= coin:
                    dp[j] += dp[j - coin]
        return dp[amount-1]

s = Solution()
print(s.change(5, [1, 2, 5]))
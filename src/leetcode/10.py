'''
‘.’和‘*’正则表达式匹配，
'''

class Solution:
    def isMatch(self, s: str, p: str) -> bool:
        dp = [[False for _ in range(len(p) + 1)] for _ in range(len(s) + 1)]

        dp[0][0] = True

        for i in range(1, len(s) + 1):
            for j in range(1, len(p) + 1):
                if p[j] in ['.', s[i]]:
                    dp[i][j] = dp[i-1][j-1]
                elif p[j] == '*':
                    if p[j-1] in ['.', s[i]]:
                        dp[i][j] = dp[i - 1][j] or dp[i][j - 2]
                    else:
                        dp[i][j] = dp[i][j - 2]
        return dp[len(s)][len(p)]

s = Solution()
s.isMatch('123', '.23')
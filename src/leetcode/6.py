class Solution:
    def convert(self, s: str, numRows: int) -> str:
        res = ['' for _ in range(numRows)]
        # 向下
        direction = 1
        row = 0
        for i in range(len(s)):
            res[row] += s[i]
            if not -1 < row + direction < numRows:
                direction = -direction
            row += direction
        return ''.join(res)


s = Solution()
print(s.convert('LEETCODEISHIRING', 4))
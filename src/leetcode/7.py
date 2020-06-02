class Solution:
    def reverse(self, x: int) -> int:
        flag = -1 if x < 0 else 1
        x = abs(x)
        l = []
        result = 0
        level = 1
        while x:
            remainder = x % 10
            l.append(remainder)
            x = x // 10
        for i in range(len(l) - 1, -1, -1):
            result += l[i] * level
            level *= 10
        if result * flag > 2 ** 31 - 1 or result * flag < -2 ** 31:
            return 0
        return result * flag

s = Solution()
print(s.reverse(1534236469))
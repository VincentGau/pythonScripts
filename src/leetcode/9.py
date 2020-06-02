class Solution:
    def isPalindrome(self, x: int) -> bool:
        if x < 0:
            return False
        l = []
        while x:
            remainder = x % 10
            x = x // 10
            l.append(remainder)
        left = 0
        right = len(l) - 1
        while left < right:
            if l[left] != l[right]:
                return False
            left += 1
            right -= 1
        return True



s = Solution()
print(s.isPalindrome(12321))
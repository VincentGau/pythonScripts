class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        dict = {}
        maxLength = 1
        left = 0
        if not len(s):
            return 0
        for i in range(len(s)):
            if s[i] not in dict or dict[s[i]] < left:
                dict[s[i]] = i
                maxLength = max(maxLength, i - left + 1)
            else:
                left = dict[s[i]] + 1
                dict[s[i]] = i
        return maxLength

s = Solution()
print(s.lengthOfLongestSubstring('abcabcbb'))


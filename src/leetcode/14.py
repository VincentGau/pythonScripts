from typing import List

# 对数组排序 得到首尾两个字符串的公共前缀即为所求

class Solution:
    def longestCommonPrefix(self, strs: List[str]) -> str:
        if not strs:
            return ''
        if len(strs) == 1:
            return strs[0]
        strs.sort()
        print(strs)
        res = ''
        for i, c in enumerate(strs[0]):
            if c == strs[-1][i]:
                res += c
            else:
                break

        return res

s = Solution()
print(s.longestCommonPrefix(["flower","flow","flight"]))
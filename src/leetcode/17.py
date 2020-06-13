from typing import List


'''
电话号码组合， 递归方法；
'''

class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        if not digits:
            return []
        s = ['', '', 'abc', 'def', 'ghi', 'jkl', 'mno', 'pqrs', 'tuv', 'wxyz']
        if len(digits) == 1:
            return list(s[int(digits[0])])
        res = []
        for c in s[int(digits[0])]:
            for t in self.letterCombinations(digits[1:]):
                res.append(c + t)
        return res


s = Solution()
print(s.letterCombinations("23"))


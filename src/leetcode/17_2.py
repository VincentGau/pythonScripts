from typing import List


class Solution:
    def letterCombinations(self, digits: str) -> List[str]:
        s = ['', '', 'abc', 'def', 'ghi', 'jkl', 'mno', 'pqrs', 'tuv', 'wxyz']

        def backtrack(cur, next_digits):
            if not next_digits:
                res.append(cur)
            else:
                for c in s[int(next_digits[0])]:
                    backtrack(cur + c, next_digits[1:])
        res = []
        if digits:
            backtrack('', digits)
        return res


s = Solution()
print(s.letterCombinations("23"))


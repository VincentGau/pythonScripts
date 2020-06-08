from typing import List


class Solution:
    def lemonadeChange(self, bills: List[int]) -> bool:
        five = 0
        ten = 0
        twenty = 0
        for i in bills:
            if i == 5:
                five += 1
            if i == 10:
                if five > 0:
                    five -= 1
                    ten += 1
                else:
                    return False
            if i == 20:
                if ten > 0 and five > 0:
                    twenty += 1
                    ten -= 1
                    five -= 1
                elif ten == 0 and five > 3:
                    twenty += 1
                    five -= 3
                else:
                    return False
        return True

s = Solution()
print(s.lemonadeChange([5,5,10,10,20]))
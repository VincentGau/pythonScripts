from typing import List
'''

'''

class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:
        dict = {}
        for i in range(len(nums)):
            if nums[i] in dict:
                return [dict[nums[i]], i]
            else:
                dict[target-nums[i]] = i

s = Solution()
# print(s.twoSum([3,3], 6))
print(s.twoSum([2, 7, 9, 11], 11))
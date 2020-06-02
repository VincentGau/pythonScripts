from typing import List


class Solution:
    def findMedianSortedArrays(self, nums1: List[int], nums2: List[int]) -> float:
        nums3 = []
        i, j = 0, 0
        len1 = len(nums1)
        len2 = len(nums2)
        while i < len1 and j < len2:
            if nums1[i] < nums2[j]:
                nums3.append(nums1[i])
                i += 1
            else:
                nums3.append(nums2[j])
                j += 1

        while i < len1:
            nums3.append(nums1[i])
            i += 1
        while j < len2:
            nums3.append(nums2[j])
            j += 1
        if len(nums3) % 2:
            return nums3[len(nums3) // 2]
        else:
            return (nums3[len(nums3) // 2] + nums3[len(nums3) // 2 - 1]) / 2

s = Solution()
print(s.findMedianSortedArrays([1, 2], [3, 4]))
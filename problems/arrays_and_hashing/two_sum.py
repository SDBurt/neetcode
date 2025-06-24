# https://leetcode.com/problems/two-sum/
from typing import List


class Solution:
    def twoSum(self, nums: List[int], target: int) -> List[int]:

        indx = {}

        for i, n in enumerate(nums):
            needed = target - n
            if needed in indx:
                return [indx[needed], i]

            indx[n] = i

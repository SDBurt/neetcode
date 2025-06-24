# https://leetcode.com/problems/contains-duplicate/
from typing import List


class Solution:
    def containsDuplicate(self, nums: List[int]) -> bool:

        if (len(nums) == 0 or len(nums) == 1):
            return False

        s = set()

        for n in nums:
            if n in s:
                return True
            s.add(n)
        return False

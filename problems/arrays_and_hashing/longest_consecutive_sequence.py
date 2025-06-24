# https://leetcode.com/problems/longest-consecutive-sequence/

from typing import List


class Solution:
    def longestConsecutive(self, nums: List[int]) -> int:

        if len(nums) == 0:
            return 0

        s = set(nums)
        longest = 0
        for n in s:

            # is the start of a sequence
            if n-1 not in s:
                length = 1
                while (n + length) in s:
                    length += 1
                longest = max(length, longest)

        return longest

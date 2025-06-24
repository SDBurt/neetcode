# https://leetcode.com/problems/product-of-array-except-self/
from typing import List


class Solution:
    def productExceptSelf(self, nums: List[int]) -> List[int]:

        num_len = len(nums)
        ans = [1]*num_len

        prefix = 1
        for i in range(num_len):  # O(n)
            ans[i] = prefix
            prefix *= nums[i]

        postfix = 1
        for j in range(num_len-1, -1, -1):  # O(n)
            ans[j] *= postfix
            postfix *= nums[j]

        return ans

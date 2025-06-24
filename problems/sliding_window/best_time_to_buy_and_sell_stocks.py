from typing import List


class Solution:
    def maxProfit(self, prices: List[int]) -> int:
        res = 0
        lowest_so_far = prices[0]
        for price in prices:
            if price < lowest_so_far:
                lowest_so_far = price

            res = max(res, price - lowest_so_far)

        return res

from typing import List


class Solution:
    def maxArea(self, height: List[int]) -> int:
        """Use two pointers that move towards each other
        depending on which pointer height is less.

        O(n) solution

        """
        i = 0
        j = len(height)-1
        result = 0

        while i < j:

            result = max(result, (j - i) * min(height[i], height[j]))
            if height[i] < height[j]:
                i += 1
            else:
                j -= 1  # height[i] >= height[j]

        return result

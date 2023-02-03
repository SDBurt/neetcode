# https://leetcode.com/problems/valid-anagram/
from typing import List


class Solution:
    def isAnagram(self, s: str, t: str) -> bool:

        if len(s) != len(t):
            return False

        x = {}
        y = {}

        for i in range(len(s)):
            x[s[i]] = 1 + x.get(s[i], 0)
            y[t[i]] = 1 + y.get(t[i], 0)

        return x == y

# https://leetcode.com/problems/group-anagrams/
from typing import List
from collections import defaultdict


class Solution:
    def groupAnagrams(self, strs: List[str]) -> List[List[str]]:

        res = defaultdict(list)  # mapping charCount to list of Anagrams

        for s in strs:
            count = [0] * 26  # one for each character, a ... z

            for c in s:

                count[ord(c) - ord("a")] += 1

            res[tuple(count)].append(s)

        return res.values()

        # O(m * n) solution

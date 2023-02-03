
"""
https://www.lintcode.com/problem/659

Example:
    Input: ["lint","code","love","you"]
    Output: ["lint","code","love","you"]
"""
from typing import List


class Solution:

    def encode(self, strs: List[str]) -> str:
        """
        @param: strs: a list of strings
        @return: encodes a list of strings to a single string.
        """
        payload = ""
        for s in strs:
            payload += str(len(s)) + "#" + s

        return payload

    def decode(self, s: str):
        """
        @param: str: A string
        @return: dcodes a single string to a list of strings
        """

        res = []
        i = 0
        while i < len(s):
            j = i
            while s[j] != "#":
                j += 1

            # j is at the '#' character
            l = int(s[i:j])
            res.append(s[j+1: j + 1 + l])
            i = j + 1 + l
        return res

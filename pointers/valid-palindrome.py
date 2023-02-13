# https://leetcode.com/problems/valid-palindrome/

import re


class Solution:
    def isPalindrome(self, s: str) -> bool:

        if len(s) == 1:
            return True

        a = re.sub(r"[^a-zA-Z0-9]+", "", s)  # only keep alphanumeric
        a = a.lower()  # make lower after removing characters

        start = 0
        end = len(a)-1

        if len(a) == 0 or end <= start:
            return True

        while start < end:
            if a[start] != a[end]:
                return False

            start += 1
            end -= 1

        return True

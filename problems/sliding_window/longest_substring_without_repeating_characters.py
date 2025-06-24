class Solution:
    def lengthOfLongestSubstring(self, s: str) -> int:
        """Create a window and expand it until you find another character in the substring
        Once you find it, slice the string from the start to the current position and find the
        duplicate character -- updating the starting point to just after.
        """
        res = 0

        t = ""
        st = 0
        for i, c in enumerate(s):

            # character is in the substring
            if c in t:

                res = max(res, len(t))
                r = s[st:i]

                st = st + r.index(c) + 1  # get the new starting index
                t = s[st:i+1]  # +1 to include the current character

            else:
                t += c

        res = max(res, len(t))

        return res

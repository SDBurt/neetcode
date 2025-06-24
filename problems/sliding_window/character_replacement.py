class Solution:
    def characterReplacement(self, s: str, k: int) -> int:
        """
        - Lowest count character?
        - Instances between characters?

        While keeping track of the start of the window, expand the window size
        while the non-max-instance characters is less than k. Once greater than k,
        move the left of the window (l) and decrement the character count of l
        """

        l = 0

        result = 0
        counts = dict()
        max_freq = 0

        for r in range(len(s)):

            # update count
            counts[s[r]] = 1 + counts.get(s[r], 0)
            max_freq = max(max_freq, counts[s[r]])

            # if width is > allowed, move left pointer and remove character count
            if (r - l + 1) - max_freq > k:
                counts[s[l]] -= 1
                l += 1

            result = max(result, r - l + 1)

        return result

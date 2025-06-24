from typing import List


class Solution:
    def threeSum(self, nums: List[int]) -> List[List[int]]:
        """Separate the numbers into positive, negative, and zero numbers.
        Then, go through the cases where the numbers contain a zero, are all zero, contain two positive, 
        and contain two negative.

        """

        # This was the largest speedup.
        # Adding values as sorted list tuples went from beating ~7% to beating ~82%
        results = set()

        p = []
        n = []
        z = []

        for i in nums:
            if (i > 0):
                p.append(i)
            elif (i < 0):
                n.append(i)
            else:
                z.append(i)

        P = set(p)
        N = set(n)

        if (len(z) > 2):
            results.add(tuple([0, 0, 0]))

        # Case len(z) > 0
        if (len(z) > 0):
            for pos in P:
                if -pos in N:
                    results.add(tuple(sorted([-pos, 0, pos])))

        # Two positives, look for target negative
        len_p = len(p)
        for i in range(len_p-1):
            for j in range(i+1, len_p):
                tn = -1 * (p[i] + p[j])
                if tn in N:
                    results.add(tuple(sorted([tn, p[i], p[j]])))

        # Two negatives, look for target positive
        len_n = len(n)
        for i in range(len_n-1):
            for j in range(i+1, len_n):
                tp = -1 * (n[i] + n[j])

                if tp in P:
                    results.add(tuple(sorted([n[i], n[j], tp])))

        return results

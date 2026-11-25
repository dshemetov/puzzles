import sys
from collections import deque


def p1703(nums: list[int], k: int) -> int:
    """1703. Minimum Adjacent Swaps for K Consecutive Ones https://leetcode.com/problems/minimum-adjacent-swaps-for-k-consecutive-ones/

    Lesson learned:
    - The first solution is not fast enough, but has the right general idea. It
      uses a sliding window of size k that records the indices of the 1s and finds
      the the absolute value of the distances to the median index in that window.
    - The second solution makes two changes. The first is to change focus from
      storing the indices of the 1s to storing the gaps between the indices of the
      1s. This is because the absolute value distance to the median has a formula
      in terms of the differences between the indices. For example, with nums =
      [1, 1, 0, 0, 1, 0, 1, 0, 1], we have gaps = [1, 3, 2, 2], so for k = 5, the
      distance to the median (the third 1) is 1 + 2 * 3 + 2 * 2 + 2 = 13. In
      general, we have

          av(j)   = sum_{i=0}^{k-2} min(i + 1, k - (i + 1)) * gaps[j + i]

      Furthermore, d1(j) = av(j) - av(j-1) and d2(j) = d1(j) - d1(j-1) can be
      expressed as

          d1(j)   = - sum_{i=0}^{k//2 - 1} gaps[j + i - 1] +                          if k is odd
                      sum_{i=k//2}^{k-1} gaps[j + i - 1],
                  = - sum_{i=0}^{k//2 - 1} gaps[j + i - 1] +                          else
                      sum_{i=k//2 + 1}^{k-1} gaps[j + i - 1],
          d2(j)   = gaps[j] - gaps[j + k//2] - gaps[j + k//2 + 1] + gaps[j + k],      if k is odd
                  = gaps[j] - 2 * gaps[j + k//2] + gaps[j + k],                       else

      This means that if we calculate the first two absolute value distances, we
      can calculate the subsequent ones via the formula

          av(j)   = av(j-1) + d1(j-1) + d2(j-1),          j >= 2
          d1(1)   = av(1) - av(0).

      This update step requires us to sum only up to 4 elements from the gaps
      array, as opposed to k.
    - The absolute value distance needs a correction to equal the swap distance

          av      = swap - T(L) - T(R), where T(x) = x * (x + 1) // 2

      where L, R are number of neighbors on the left and right of the median,
      respectively. For example, if the k-stack is [1, 1, 0, 0, 1, 0, 1], the
      absolute value distance to the median is 9, while the actual swaps needed is
      5. The correction factor can be found T(L) + T(R) = T(2) + T(1) = 3 + 1 = 4.
    - I solved this problem on my own, so I feel pretty proud of it.
    - Taking a look at other people's solutions, I see simpler approaches. For
      example, it turns out that the absolute value distance to the median can be
      expressed as

          av(j)   = sum(pos[j+k//2:j+k]) - sum(pos[j:j+k//2])
          pos(j)  = position of the jth 1 in nums

      from which it would be much easier to calculate the iterative approach. The
      way to arrive at this, is to notice that the median point has half the 1s to
      its left and half to its right.
    - There is a competitive programming trick to convert a problem from "min sum
      of moves to make numbers consecutive" to "max sum of moves to a single
      point" and that is to transform pos(j) to pos(j) - j. This is because

          sum pos(j) - j = sum pos(j) - sum j = sum pos(j) - k * (k + 1) // 2

      which is the correction factor we discused above.

    Examples
    --------
    >>> p1703([1, 0, 0, 1, 0, 1], 2)
    1
    >>> p1703([1, 0, 0, 0, 0, 0, 1, 1], 3)
    5
    >>> p1703([1, 1, 0, 1], 2)
    0
    >>> p1703([0, 0, 0, 1, 0, 1, 1, 0, 1], 3)
    1
    >>> p1703([0, 0, 0, 1, 0, 1, 1, 0, 1], 4)
    2
    >>> p1703([1, 0, 1, 0, 1, 0, 0, 0, 1], 4)
    6

    """
    if len(nums) == k or k == 1:
        return 0

    def triangular_number(n: int) -> int:
        return n * (n + 1) // 2

    mid1, mid2 = k // 2 - 1, k // 2
    if k % 2 == 0:
        correction_factor = triangular_number(mid1) + triangular_number(mid2)
    else:
        correction_factor = 2 * triangular_number(mid2)

    def calculate_swaps(stack: deque[int]) -> int:
        """Calculate the swaps needed to get to the median(s) of the stack.

        The stack represents the indices of the 1s in the array.
        """
        return sum(abs(stack[mid2] - i) for i in stack)

    stack = deque()
    s = 0
    m = sys.maxsize
    for i, n in enumerate(nums):
        if n == 1:
            stack.append(i)
            if stack and len(stack) > k:
                s = s - stack.popleft()
            if len(stack) == k:
                m = min(m, calculate_swaps(stack))

    return m - correction_factor

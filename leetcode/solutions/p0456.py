def p456(nums: list[int]) -> bool:
    """456. 132 Pattern https://leetcode.com/problems/132-pattern/

    Lessons learned:
    - Another opportunity to put monotonic stacks to use. I still don't know
    exactly when to use them, probably need some more practice.

    Examples
    --------
    >>> p456([1, 2, 3, 4])
    False
    >>> p456([3, 1, 4, 2])
    True
    >>> p456([-1, 3, 2, 0])
    True
    >>> p456([1, 2, 0, 3, -1, 4, 2])
    True
    >>> p456([1, 3, -1, 1, 1])
    False
    >>> p456([-2, 1, -2])
    False

    """
    span_stack = [[nums[0], nums[0]]]

    for new_val in nums[1:]:
        top_span = span_stack.pop()
        if new_val < top_span[0]:
            span_stack.append(top_span)
            span_stack.append([new_val, new_val])
        elif top_span[0] < new_val < top_span[1]:
            return True
        elif new_val > top_span[1]:
            top_span[1] = new_val
            while span_stack:
                next_span = span_stack.pop()
                if top_span[1] <= next_span[0]:
                    span_stack.append(next_span)
                    break
                if next_span[0] < top_span[1] < next_span[1]:
                    return True
                if next_span[1] <= top_span[1]:
                    continue
            span_stack.append(top_span)
        else:
            span_stack.append(top_span)
    return False

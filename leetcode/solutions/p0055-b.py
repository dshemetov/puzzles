def p55b(nums: list[int]) -> bool:
    n = len(nums)
    current = n - 1
    for i in range(n - 2, -1, -1):
        step = nums[i]

        if i + step >= current:
            current = i

    return current == 0

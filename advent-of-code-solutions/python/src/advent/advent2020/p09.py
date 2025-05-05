def solve_a(s: str) -> int:
    nums = [int(line) for line in s.split("\n")]
    for i, x in enumerate(nums):
        if i < 25:
            continue
        valid_nums = make_pairs(nums[i - 25 : i])
        if x not in valid_nums:
            break
    return x


def make_pairs(nums):
    from itertools import product

    return set([x + y for x, y in product(nums, repeat=2) if x != y])


def solve_b(s: str) -> int:
    nums = [int(line) for line in s.split("\n")]
    for i in range(len(nums)):
        for j in range(i, len(nums)):
            if sum(nums[i:j]) == 138879426:
                return max(nums[i:j]) + min(nums[i:j])

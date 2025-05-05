# TODO: Implement a merge-deep function.
# TODO: Implement a deep-merge function.
# TODO: Find a cycle in a linked list.


def find_first_repeated_element(arr):
    """
    Examples:
    >>> find_first_repeated_element([10, 5, 3, 4, 3, 5, 6])
    3
    >>> find_first_repeated_element([6, 10, 5, 4, 9, 120, 4, 6, 10])
    4
    >>> find_first_repeated_element([1, 2, 3])
    -1
    """
    seen = {}
    for x in arr:
        if x in seen:
            return x
        else:
            seen[x] = True
    return -1


def count_subarrays_with_sum_p(arr: list[int], p: int) -> int:
    """
    Count contiguous subarrays with sum p.

    Examples:
    >>> subarrays_with_sum_p([10, 2, -2, -20, 10], -10)
    1
    >>> subarrays_with_sum_p([9, 4, 20, 3], 33)
    1
    """
    count = 0
    for i in range(len(arr)):
        for j in range(i + 1, len(arr) + 1):
            if sum(arr[i:j]) == p:
                count += 1
    return count


def brute_force_greatest_product(arr: list[int]):
    """
    Examples:
    >>> brute_force_greatest_product([2, 2, 4, 5, 9])
    45
    >>> brute_force_greatest_product([1, 3, 4, 7, 10])
    70
    >>> brute_force_greatest_product([3, 3, 4, 7, 10])
    70
    >>> brute_force_greatest_product([-300, -3, 4, 7, 10])
    900
    """
    if len(arr) < 2:
        return None

    if len(arr) == 2:
        return arr[0] * arr[1]

    arr.sort()

    if arr[0] > 0:
        return arr[-1] * arr[-2]

    if arr[-1] < 0:
        return arr[0] * arr[1]

    return max(arr[0] * arr[1], arr[-1] * arr[-2])

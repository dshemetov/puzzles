"""9. https://adventofcode.com/2024/day/9"""

import numba as nb
import numpy as np
from numba import int8, int32


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    1928
    """
    s = s.strip("\n")

    # Parse input and calculate total size
    nums = np.array([int(c) for c in s], dtype=np.int8)
    total_size = sum(nums)

    return solve_a_numba(nums, total_size)


@nb.njit(int32(int8[:], int32), cache=True)
def solve_a_numba(nums: np.ndarray, total_size: int) -> int:
    # Create disk representation directly
    disk = np.full(total_size, -1, dtype=np.int16)
    pos = 0
    # The input is a list of numbers that alternative between file size and free
    # space size.
    for i, n in enumerate(nums):
        # If the size is 0, skip.
        if n == 0:
            continue

        # Even index is file ID.
        if i % 2 == 0:
            file_id = np.int16(i // 2)
            disk[pos : pos + n] = file_id
        else:
            disk[pos : pos + n] = -1
        pos += n

    # Two-pointer defragmentation
    left = 0
    right = total_size - 1

    while left < right:
        # Find next free space from left
        while left < total_size and disk[left] != -1:
            left += 1

        # Find next file block from right
        while right >= 0 and disk[right] == -1:
            right -= 1

        # If there are no more free spaces or file blocks, stop.
        if left >= right:
            break

        # Move the file block to the free space.
        disk[left] = disk[right]
        disk[right] = -1
        left += 1
        right -= 1

    # Calculate checksum
    checksum = 0
    for pos, file_id in enumerate(disk):
        if file_id != -1:
            checksum += pos * file_id

    return checksum


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    2858
    """
    s = s.strip("\n")

    # Parse input and calculate total size
    nums = np.array([int(c) for c in s], dtype=np.int8)
    total_size = sum(nums)

    return solve_b_numba(nums, total_size)


@nb.njit(int32(int8[:], int32), cache=True)
def solve_b_numba(nums: np.ndarray, total_size: int) -> int:
    # Pre-allocate arrays for file and free space tracking
    max_files = (total_size + 1) // 2
    file_positions = [0] * max_files
    file_sizes = [0] * max_files

    free_positions = []
    free_sizes = []

    pos = 0
    file_count = 0

    for i, n in enumerate(nums):
        if n == 0:
            pos += n
            continue

        if i % 2 == 0:  # File (even indices are files)
            file_id = i // 2  # 0-based file ID
            file_positions[file_id] = int(pos)
            file_sizes[file_id] = int(n)
            file_count = max(file_count, file_id + 1)
        else:  # Free space (odd indices are free space)
            free_positions.append(int(pos))
            free_sizes.append(int(n))
        pos += n

    # Resize arrays to actual size
    file_positions = file_positions[:file_count]
    file_sizes = file_sizes[:file_count]

    # Process files from highest ID to lowest
    for file_id in range(file_count - 1, -1, -1):
        file_pos = file_positions[file_id]
        file_size = file_sizes[file_id]

        # Find leftmost free space that can fit this file
        for i, free_pos in enumerate(free_positions):
            if free_pos >= file_pos:  # Don't move right
                break

            if free_sizes[i] >= file_size:
                # Move the file
                file_positions[file_id] = free_pos

                # Update free space
                if free_sizes[i] == file_size:
                    # Exact fit - remove free space
                    free_positions.pop(i)
                    free_sizes.pop(i)
                else:
                    # Partial fit - update free space
                    free_positions[i] += file_size
                    free_sizes[i] -= file_size
                break

    # Calculate checksum
    checksum = 0
    for file_id in range(file_count):
        pos = file_positions[file_id]
        size = file_sizes[file_id]
        for offset in range(size):
            checksum += file_id * (pos + offset)

    return checksum


test_string = """
2333133121414131402
"""

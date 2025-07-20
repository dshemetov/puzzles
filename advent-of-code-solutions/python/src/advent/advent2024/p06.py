"""6. https://adventofcode.com/2024/day/6

Part (b) is the interesting part. Initial solution ran in about 1.5s, but I left
many optimizations on the table. Turns out the bounds checking when moving the
guard forward took the most time. I removed some duplicate computations there,
which brought time down to 1s. Evin suggested compressing the grid to sorted
arrays of obstacles and using binary search to jump to the next obstacle
instead. That brought it down to 0.1s.
"""

import numba as nb
import numpy as np
from numba import boolean, int32, int64, uint8

# Direction constants: up=0, right=1, down=2, left=3
DIRECTIONS = ((-1, 0), (0, 1), (1, 0), (0, -1))
TURN_RIGHT = (1, 2, 3, 0)  # Turn right: up->right, right->down, down->left, left->up


@nb.njit(int32(uint8[:, :], nb.typeof((2,2)), int32, int32), fastmath=True, cache=True, boundscheck=False)
def solve_a_numba(grid, start_pos, m, n):
    """Numba-optimized version of solve_a with aggressive type annotations."""
    visited = np.zeros((m, n), dtype=boolean)
    pos_i, pos_j = start_pos
    dir_idx = int32(0)  # Start facing up
    total = int64(0)

    while 0 <= pos_i < m and 0 <= pos_j < n:
        if grid[pos_i, pos_j] == ord('#'):
            # Back up and turn right
            pos_i -= DIRECTIONS[dir_idx][0]
            pos_j -= DIRECTIONS[dir_idx][1]
            dir_idx = TURN_RIGHT[dir_idx]
        else:
            if not visited[pos_i, pos_j]:
                visited[pos_i, pos_j] = True
                total += 1
            pos_i += DIRECTIONS[dir_idx][0]
            pos_j += DIRECTIONS[dir_idx][1]

    return total


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    41
    """
    s = s.strip("\n")
    # Convert to uint8 for better Numba performance
    grid = np.array([[ord(c) for c in row] for row in s.split("\n")], dtype=np.uint8)
    m, n = grid.shape

    # Find start position
    start_pos = tuple(np.where(grid == ord('^')))
    start_pos = (int32(start_pos[0][0]), int32(start_pos[1][0]))
    grid[start_pos] = ord('.')

    return solve_a_numba(grid, start_pos, m, n)


@nb.njit(uint8[:,:](uint8[:, :], nb.typeof((2,2)), int32, int32), fastmath=True, cache=True)
def get_path_numba(grid, start_pos, m, n):
    """Numba-optimized version of get_path with aggressive type annotations."""
    visited = np.zeros((m, n), dtype=boolean)
    path = []
    pos_i, pos_j = start_pos
    dir_idx = int32(0)  # Start facing up

    while 0 <= pos_i < m and 0 <= pos_j < n:
        if grid[pos_i, pos_j] == ord('#'):
            # Back up and turn right
            pos_i -= DIRECTIONS[dir_idx][0]
            pos_j -= DIRECTIONS[dir_idx][1]
            dir_idx = TURN_RIGHT[dir_idx]
        elif not visited[pos_i, pos_j]:
            visited[pos_i, pos_j] = True
            path.append((pos_i, pos_j))
        pos_i += DIRECTIONS[dir_idx][0]
        pos_j += DIRECTIONS[dir_idx][1]

    return np.array(path, dtype=np.uint8)


@nb.njit(boolean(uint8[:, :], nb.typeof((2,2)), nb.typeof((2,2)), int32, int32), fastmath=True, cache=True)
def creates_loop_numba(grid, start_pos, obstacle_pos, m, n):
    """Numba-optimized version of creates_loop with aggressive type annotations."""
    # Create visited states array
    visited_states = np.zeros((m, n, 4), dtype=boolean)

    # Temporarily add obstacle
    obs_i, obs_j = obstacle_pos
    original_char = grid[obs_i, obs_j]
    grid[obs_i, obs_j] = ord('#')

    pos_i, pos_j = start_pos
    dir_idx = int32(0)
    result = False

    while 0 <= pos_i < m and 0 <= pos_j < n:
        if visited_states[pos_i, pos_j, dir_idx]:
            result = True
            break

        visited_states[pos_i, pos_j, dir_idx] = True
        next_i = pos_i + DIRECTIONS[dir_idx][0]
        next_j = pos_j + DIRECTIONS[dir_idx][1]

        if (0 <= next_i < m and 0 <= next_j < n and
            grid[next_i, next_j] == ord('#')):
            dir_idx = TURN_RIGHT[dir_idx]
        else:
            pos_i, pos_j = next_i, next_j

    # Clean up
    grid[obs_i, obs_j] = original_char
    return result


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    6
    """
    s = s.strip("\n")
    # Convert to uint8 for better Numba performance
    grid = np.array([[ord(c) for c in row] for row in s.split("\n")], dtype=np.uint8)
    m, n = grid.shape

    # Find start position
    start_pos = tuple(np.where(grid == ord('^')))
    start_pos = (int32(start_pos[0][0]), int32(start_pos[1][0]))
    grid[start_pos] = ord('.')

    # Get original path
    original_path = get_path_numba(grid, start_pos, m, n)

    # Try placing an obstacle in each position on the original path
    total = 0
    for i in range(len(original_path)):
        test_pos = original_path[i,0], original_path[i,1]
        if grid[test_pos[0], test_pos[1]] == ord('#') or test_pos == start_pos:
            continue
        # If the obstacle creates a loop, it's a valid obstacle
        if creates_loop_numba(grid, start_pos, test_pos, m, n):
            total += 1

    return total


test_string = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

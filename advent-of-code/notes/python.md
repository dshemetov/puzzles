# Python notes

- Cython was tried once, for 2022 day 11 part b (about 8ms). A scalar Numba loop that follows each item on its own is faster (about 4ms) and needs no build step, so Cython is not worth it for these puzzles. The old version is in git history.
- Cython also did not help for 2022 day 12: the bottleneck is `heapq`, and Cython/Numba have no resizable array to replace it with.

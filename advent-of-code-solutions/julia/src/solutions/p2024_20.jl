"""20. https://adventofcode.com/2024/day/20

This is a neat problem. The path-finding is a red-herring, since there is only
one path. The real work is in finding the cheats. With the path length ~10_000,
I considered a few approaches:

- For part (a), the Manhattan ball is only 2 units, so I could just look at all
  the points 2 units away from each point in the path. This took about 0.05
  seconds.
- For part (b), the naive approach is to check all pairs of points in the path,
  which is O(n^2), so O(100M) operations. This takes about 5 seconds.
- Checking a 20 unit ball around each point, the complexity is about O(200
  * n = 2M) operations. Despite the drastic estimated operation reduction, it
  still took 2.5s (bad estimates due to constants, more expensive operations
  like hash maps, etc.). Pre-computing the ball pattern didn't really help, but
  it was clean, so I kept it. Adding a sizehint! to the seen_cheats gave about
  ~0.3s. Adding early bound checks and wall checks added another ~0.3s. Finally,
  realizing that I only need half the ball by symmetry brought it down to ~1s.
  Out of ideas after that, but 1s is my upper limit goal for these problems.
- I thought about k-d trees and ball trees for part (b), but they felt too
  heavy.
"""

function solve(input::Question{2024,20,'a'})
    if input.s == ""
        time_diff_thresh = 2
        s = test_string_2024_20
    else
        time_diff_thresh = 100
        s = input.s
    end
    grid = string_to_char_matrix(strip(s, '\n'))
    m, n = size(grid)
    s = Tuple(findfirst(==('S'), grid))
    t = Tuple(findfirst(==('E'), grid))

    # Get maze path (there's only one)
    dist, prev_map = maze_solver(grid, s, t, m, n)
    path = []
    current = t
    while current != s
        push!(path, current)
        current = prev_map[current]
    end
    push!(path, s)
    reverse!(path)
    path_map = Dict{Tuple{Int,Int},Int}((x, y) => i for (i, (x, y)) in enumerate(path))

    # Count cheats by trying all points 2 units away from each point in the path
    total_cheats = 0
    seen_cheats = Set{Tuple{Int,Int}}()
    for (i, (x, y)) in enumerate(path)
        # Get Manhattan ball of radius 2
        neighbors = [(x + dx, y + dy) for dx in -2:2 for dy in (-2+abs(dx)):(2-abs(dx))]
        for (x2, y2) in neighbors
            if !haskey(path_map, (x2, y2))
                continue
            end
            j = path_map[(x2, y2)]
            if (i, j) in seen_cheats
                continue
            end
            # The time saved is the difference in the track position minus the
            # time taken to walk that distance in Manhattan distance.
            time_diff = abs(i - j) - 2
            if time_diff >= time_diff_thresh
                push!(seen_cheats, (i, j))
                push!(seen_cheats, (j, i))
                total_cheats += 1
            end
        end
    end
    return total_cheats
end

function maze_solver(grid, s, t, m, n)
    queue = [(0, s[1], s[2])]
    visited = Set{Tuple{Int,Int}}()
    prev_map = Dict{Tuple{Int,Int},Tuple{Int,Int}}()
    while !isempty(queue)
        dist, x, y = popfirst!(queue)
        if x == t[1] && y == t[2]
            return dist, prev_map
        end
        for (dx, dy) in [(0, 1), (1, 0), (0, -1), (-1, 0)]
            nx, ny = x + dx, y + dy
            if 1 <= nx <= m && 1 <= ny <= n && grid[nx, ny] != '#' && (nx, ny) ∉ visited
                push!(queue, (dist + 1, nx, ny))
                prev_map[(nx, ny)] = (x, y)
                push!(visited, (nx, ny))
            end
        end
    end
    return 0, prev_map
end

function solve(input::Question{2024,20,'b'})
    if input.s == ""
        time_diff_thresh = 50
        s = test_string_2024_20
    else
        time_diff_thresh = 100
        s = input.s
    end
    grid = string_to_char_matrix(strip(s, '\n'))
    m, n = size(grid)
    s = Tuple(findfirst(==('S'), grid))
    t = Tuple(findfirst(==('E'), grid))
    # Get maze path (there's only one)
    dist, prev_map = maze_solver(grid, s, t, m, n)
    path = []
    current = t
    while current != s
        push!(path, current)
        current = prev_map[current]
    end
    push!(path, s)
    reverse!(path)
    path_map = Dict{Tuple{Int,Int},Int}([(x, y) => i for (i, (x, y)) in enumerate(path)])

    # Pre-compute Manhattan ball of radius 20 pattern
    # only need half the ball, by symmetry
    ball_pattern = [(dx, dy) for dx in 0:20 for dy in (-20+abs(dx)):(20-abs(dx))]

    # Count cheats by trying all points 20 units away from each point in the path
    seen_cheats = Set{Tuple{Int,Int}}()
    sizehint!(seen_cheats, 50_000)
    total_cheats = 0
    for (i, (x, y)) in enumerate(path)
        for (dx, dy) in ball_pattern
            x2, y2 = x + dx, y + dy
            if !(1 <= x2 <= m && 1 <= y2 <= n)
                continue
            end
            if grid[x2, y2] == '#'
                continue
            end
            j = path_map[(x2, y2)]
            # The time saved is the difference in the track position minus
            # the time taken to walk that distance in Manhattan distance.
            time_diff = abs(i - j) - (abs(x - x2) + abs(y - y2))
            if time_diff >= time_diff_thresh && (i, j) ∉ seen_cheats
                push!(seen_cheats, (i, j))
                push!(seen_cheats, (j, i))
                total_cheats += 1
            end

        end
    end
    return total_cheats
end


test_string_2024_20 = """
###############
#...#...#.....#
#.#.#.#.#.###.#
#S#...#.#.#...#
#######.#.#.###
#######.#.#...#
#######.#.###.#
###..E#...#...#
###.#######.###
#...###...#...#
#.#####.#.###.#
#.#...#.#.#...#
#.#.#.#.#.#.###
#...#...#...###
###############
"""
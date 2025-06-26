"""20. https://adventofcode.com/2024/day/20

I learned a lot by doing this problem. The path-finding is a red-herring, since
there is only one path through the maze. The real work is in finding the cheats.
With the maze path being length ~10_000, there are two main approaches:

- Check pairs of points along the path. If they're within the radius and the
  cheat is above threshold, count it. This takes O(n^2 = 100M) operations.
- Check all points in a ball around each point in the path. If they're within
  the radius and the cheat is above threshold, count it. This takes O(200 * n =
  2M) operations (however, these operations involve hash maps).

You can optimize both of these a bit:

- For the pairwise approach, you can make sure that the i and j pairs are always
  time_diff_thresh apart, to improve the O(n^2) constant.
- For the ball approach, you can check only half the ball (due to symmetry) and
  improve the O(n) constant by a factor of 2.

However, both of these improvements are no match for using Julia correctly
(surprise!). There were two key ideas here:

- Consulting a friend who's more proficient with Julia, he prodded me to type
  annotate everything. While the compiler can deduce types, it's better to
  annotate them explicitly. This made the above algorithmic optimizations moot
  and brought the time to about ~1s for both approaches.
- Removing hash maps and replacing them with pre-allocated matrices was another
  huge gain. It brought the time down to ~20ms for both approaches. Turns out,
  hash maps are CPU cache unfriendly, more expensive than a matrix lookup, and
  don't play well with vectorization/SIMD.
"""

function solve(input::Question{2024,20,'a'}, method::String="pairwise")
    if input.s == ""
        time_diff_thresh = 50
        s = test_string_2024_20
    else
        time_diff_thresh = 100
        s = input.s
    end
    radius = 2

    if method == "ball"
        return ball_cheat_solver(strip(s, '\n'), radius, time_diff_thresh)
    elseif method == "pairwise"
        return pairwise_cheat_solver(strip(s, '\n'), radius, time_diff_thresh)
    else
        error("Invalid method: $method")
    end
end

function maze_solver(grid, s, t)
    m::Int, n::Int = size(grid)
    queue::Vector{Tuple{Int,Int,Int}} = [(0, s[1], s[2])]
    visited::Set{Tuple{Int,Int}} = Set{Tuple{Int,Int}}()
    prev_map::Dict{Tuple{Int,Int},Tuple{Int,Int}} = Dict{Tuple{Int,Int},Tuple{Int,Int}}()
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

function solve(input::Question{2024,20,'b'}, method::String="pairwise")
    if input.s == ""
        time_diff_thresh = 50
        s = test_string_2024_20
    else
        time_diff_thresh = 100
        s = input.s
    end
    radius = 20

    if method == "pairwise"
        return pairwise_cheat_solver(strip(s, '\n'), radius, time_diff_thresh)
    elseif method == "ball"
        return ball_cheat_solver(strip(s, '\n'), radius, time_diff_thresh)
    else
        error("Invalid method: $method")
    end
end

function ball_cheat_solver(s::AbstractString, radius::Int, time_diff_thresh::Int)
    grid::Matrix{Char} = stack(split(s, "\n"))
    m, n = size(grid)
    st::Tuple{Int,Int} = Tuple(findfirst(==('S'), grid))
    ta::Tuple{Int,Int} = Tuple(findfirst(==('E'), grid))
    # Get maze path (there's only one)
    dist::Int, prev_map::Dict{Tuple{Int,Int},Tuple{Int,Int}} = maze_solver(grid, st, ta)
    path::Vector{Tuple{Int,Int}} = []
    current::Tuple{Int,Int} = ta
    while current != st
        push!(path, current)
        current = prev_map[current]
    end
    push!(path, st)
    reverse!(path)

    # The matrix here doesn't improve much over a dictionary.
    path_map::Matrix{Int} = fill(-1, m, n)
    for (i, (x, y)) in enumerate(path)
        path_map[x, y] = i
    end

    # Pre-compute Manhattan ball pattern
    # only need half the ball, by symmetry
    ball_pattern::Vector{Tuple{Int,Int}} = [(dx, dy) for dx in 0:radius for dy in (-radius+abs(dx)):(radius-abs(dx))]

    # Count cheats by trying all points in the ball pattern from each point in the path
    seen_cheats::Matrix{Bool} = fill(false, length(path), length(path))
    total_cheats::Int = 0
    for (i, (x, y)) in enumerate(path)
        for (dx, dy) in ball_pattern
            x2::Int, y2::Int = x + dx, y + dy
            if !(1 <= x2 <= m && 1 <= y2 <= n)
                continue
            end
            if grid[x2, y2] == '#'
                continue
            end
            j::Int = path_map[x2, y2]
            if j == -1
                continue
            end
            # The time saved is the difference in the track position minus
            # the time taken to walk that distance in Manhattan distance.
            time_diff::Int = abs(i - j) - (abs(x - x2) + abs(y - y2))
            if time_diff >= time_diff_thresh && !seen_cheats[i, j]
                seen_cheats[i, j] = true
                seen_cheats[j, i] = true
                total_cheats += 1
            end

        end
    end
    return total_cheats
end

function pairwise_cheat_solver(s::AbstractString, radius::Int, time_diff_thresh::Int)
    grid::Matrix{Char} = stack(split(s, "\n"))
    m, n = size(grid)
    st::Tuple{Int,Int} = Tuple(findfirst(==('S'), grid))
    ta::Tuple{Int,Int} = Tuple(findfirst(==('E'), grid))
    # Get maze path (there's only one)
    dist::Int, prev_map::Dict{Tuple{Int,Int},Tuple{Int,Int}} = maze_solver(grid, st, ta)
    path::Vector{Tuple{Int,Int}} = []
    current::Tuple{Int,Int} = ta
    while current != st
        push!(path, current)
        current = prev_map[current]
    end
    push!(path, st)
    reverse!(path)

    cheats::Int = 0
    for j::Int in time_diff_thresh:length(path)
        for i::Int in 1:j-time_diff_thresh
            x1::Int, y1::Int = path[i]
            x2::Int, y2::Int = path[j]
            distance::Int = abs(x1 - x2) + abs(y1 - y2)
            if distance <= radius && j - i - distance >= time_diff_thresh
                cheats += 1
            end
        end
    end
    return cheats
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
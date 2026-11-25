"""20. https://adventofcode.com/2024/day/20
# Variant of d20.jl: searches a ball around each point instead of all pairs (same answers).

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

function part_a(input::AbstractString; time_diff_thresh=100)
    return ball_cheat_solver(strip(input, '\n'), 2, time_diff_thresh)
end

function part_b(input::AbstractString; time_diff_thresh=100)
    return ball_cheat_solver(strip(input, '\n'), 20, time_diff_thresh)
end

function maze_solver(grid, s, t)
    m, n = size(grid)
    queue = Tuple{Int,Int,Int}[(0, s[1], s[2])]
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

function ball_cheat_solver(s::AbstractString, radius::Int, time_diff_thresh::Int)
    grid::Matrix{Char} = stack(split(s, "\n"))
    m, n = size(grid)
    st = Tuple(findfirst(==('S'), grid))
    ta = Tuple(findfirst(==('E'), grid))
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
    path_map = fill(-1, m, n)
    for (i, (x, y)) in enumerate(path)
        path_map[x, y] = i
    end

    # Pre-compute Manhattan ball pattern
    # only need half the ball, by symmetry
    ball_pattern = Tuple{Int,Int}[(dx, dy) for dx in 0:radius for dy in (-radius+abs(dx)):(radius-abs(dx))]

    # Count cheats by trying all points in the ball pattern from each point in the path
    seen_cheats = fill(false, length(path), length(path))
    total_cheats = 0
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

function main(path)
    input = read(path, String)
    for (name, part) in (("part_a", part_a), ("part_b", part_b))
        first_call = @elapsed answer = part(input)
        println(answer)
        # The first call includes compiling. Call again (if it was quick) to time just the work.
        warm = first_call < 2 ? @elapsed(part(input)) : first_call
        println(stderr, name, ": ", round(warm, digits=4), "s (first call ", round(first_call, digits=4), "s)")
    end
end

# Only runs as a script, so `include`-ing this file in a REPL stays quiet.
if abspath(PROGRAM_FILE) == @__FILE__
    main(ARGS[1])
end

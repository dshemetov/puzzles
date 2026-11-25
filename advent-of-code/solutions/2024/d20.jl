"""20. https://adventofcode.com/2024/day/20
# Alternative approach: d20-ball.jl

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
    return pairwise_cheat_solver(strip(input, '\n'), 2, time_diff_thresh)
end

function part_b(input::AbstractString; time_diff_thresh=100)
    return pairwise_cheat_solver(strip(input, '\n'), 20, time_diff_thresh)
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

function pairwise_cheat_solver(s::AbstractString, radius::Int, time_diff_thresh::Int)
    grid::Matrix{Char} = stack(split(s, "\n"))
    m, n = size(grid)
    st = Tuple(findfirst(==('S'), grid))
    ta = Tuple(findfirst(==('E'), grid))
    # Get maze path (there's only one)
    dist::Int, prev_map::Dict{Tuple{Int,Int},Tuple{Int,Int}} = maze_solver(grid, st, ta)
    path = Tuple{Int,Int}[]
    current = ta
    while current != st
        push!(path, current)
        current = prev_map[current]
    end
    push!(path, st)
    reverse!(path)

    cheats = 0
    for j in time_diff_thresh:length(path)
        for i in 1:j-time_diff_thresh
            x1, y1 = path[i]
            x2, y2 = path[j]
            distance = abs(x1 - x2) + abs(y1 - y2)
            if distance <= radius && j - i - distance >= time_diff_thresh
                cheats += 1
            end
        end
    end
    return cheats
end

# The key=value arguments after the input file that this part declares as keyword parameters.
function params_for(part, data, extra)
    pairs = [Symbol(k) => something(tryparse(Int, v), v) for (k, v) in split.(extra, "="; limit=2)]
    return filter(p -> hasmethod(part, Tuple{typeof(data)}, (first(p),)), pairs)
end

function main(path, extra=String[])
    input = read(path, String)
    for (name, part) in (("part_a", part_a), ("part_b", part_b))
        params = params_for(part, input, extra)
        first_call = @elapsed answer = part(input; params...)
        println(answer)
        # The first call includes compiling. Call again (if it was quick) to time just the work.
        warm = first_call < 2 ? @elapsed(part(input; params...)) : first_call
        println(stderr, name, ": ", round(warm, digits=4), "s (first call ", round(first_call, digits=4), "s)")
    end
end

# Only runs as a script, so `include`-ing this file in a REPL stays quiet.
if abspath(PROGRAM_FILE) == @__FILE__
    main(ARGS[1], ARGS[2:end])
end

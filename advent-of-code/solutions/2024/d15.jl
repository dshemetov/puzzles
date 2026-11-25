# 15. https://adventofcode.com/2024/day/15


function part_a(input::AbstractString)
    s = strip(input, '\n')
    g, p = split(s, "\n\n")
    grid::Matrix{Char} = stack(split(g, "\n"), dims=1)
    path::String = replace(p, '\n' => "")

    cur = Tuple(findfirst(==('@'), grid))
    dirs = Dict('>' => (0, 1), '<' => (0, -1), '^' => (-1, 0), 'v' => (1, 0))
    for i in eachindex(path)
        dir = dirs[path[i]]
        cur_ = cur
        while true
            cur_ = cur_ .+ dir
            if grid[cur_[1], cur_[2]] == '#'
                break
            end
            if grid[cur_[1], cur_[2]] == '.'
                break
            end
        end
        if grid[cur_[1], cur_[2]] == '#'
            continue
        end
        xmin, xmax = min(cur[1], cur_[1]), max(cur[1], cur_[1])
        ymin, ymax = min(cur[2], cur_[2]), max(cur[2], cur_[2])
        grid[xmin:xmax, ymin:ymax] = circshift(grid[xmin:xmax, ymin:ymax], dir)
        cur = cur .+ dir
    end
    return score(grid)
end

function score(grid)
    m, n = size(grid)
    return sum((i - 1) * 100 + (j - 1) for i in 1:m, j in 1:n if grid[i, j] in ['O', '['])
end

function part_b(input::AbstractString)
    s = strip(input, '\n')
    s = replace(s, "#" => "##", "@" => "@.", "O" => "[]", "." => "..")
    g, p = split(s, "\n\n")
    grid::Matrix{Char} = stack(split(g, "\n"), dims=1)
    path::String = replace(p, '\n' => "")

    cur = Tuple(findfirst(==('@'), grid))
    dirs = Dict('>' => (0, 1), '<' => (0, -1), '^' => (-1, 0), 'v' => (1, 0))
    for i in eachindex(path)
        dir = dirs[path[i]]
        # These are the indices we will need to update
        affected = collect(bfs(grid, cur, dir))
        # Empty if we can't move in this direction
        if isempty(affected)
            continue
        end
        # Need to sort affected by negative of dir to move the furthest first
        affected = sort(affected, by=x -> -dir[1] * x[1] - dir[2] * x[2])
        for f in affected
            # Swap element with the one in the direction of dir
            f_ = f .+ dir
            t = grid[f_[1], f_[2]]
            grid[f_[1], f_[2]] = grid[f[1], f[2]]
            grid[f[1], f[2]] = t
        end

        cur = cur .+ dir
    end
    return score(grid)
end

function bfs(grid, s, d)
    explored = Set()
    unexplored = Set([s])
    while !isempty(unexplored)
        cur = pop!(unexplored)
        cur_ = cur .+ d
        if grid[cur_[1], cur_[2]] == '#'
            return Set()
        end
        if grid[cur_[1], cur_[2]] == '['
            if d[1] == 0 # moving right-left
                union!(unexplored, Set([cur_]))
            else
                union!(unexplored, Set([cur_, tuple(cur_ .+ [0, 1]...)]))
            end
        end
        if grid[cur_[1], cur_[2]] == ']'
            if d[1] == 0 # moving right-left
                union!(unexplored, Set([cur_]))
            else
                union!(unexplored, Set([cur_, tuple(cur_ .+ [0, -1]...)]))
            end
        end
        union!(explored, Set([cur]))
    end
    return explored
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

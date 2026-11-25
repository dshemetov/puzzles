# 8. https://adventofcode.com/2024/day/8


function part_a(input::AbstractString)
    s = strip(input, '\n')
    grid = stack([collect(row) for row in split(s, '\n')], dims=1)
    m, n = size(grid)
    antenna = Dict{Char,Vector{Tuple{Int,Int}}}()
    for i in 1:m
        for j in 1:n
            if grid[i, j] != '.'
                antenna[grid[i, j]] = push!(get(antenna, grid[i, j], []), (i, j))
            end
        end
    end

    antinodes = Set{Tuple{Int,Int}}()
    for (k, v) in antenna
        for i in 1:length(v)
            for j in i+1:length(v)
                dx = v[j][1] - v[i][1]
                dy = v[j][2] - v[i][2]
                x, y = v[j][1] + dx, v[j][2] + dy
                if 1 <= x <= m && 1 <= y <= n
                    push!(antinodes, (x, y))
                end
                x, y = v[i][1] - dx, v[i][2] - dy
                if 1 <= x <= m && 1 <= y <= n
                    push!(antinodes, (x, y))
                end
            end
        end
    end

    return length(antinodes)
end

function part_b(input::AbstractString)
    s = strip(input, '\n')
    grid = stack([collect(row) for row in split(s, '\n')], dims=1)
    m, n = size(grid)
    antenna = Dict{Char,Vector{Tuple{Int,Int}}}()
    for i in 1:m
        for j in 1:n
            if grid[i, j] != '.'
                antenna[grid[i, j]] = push!(get(antenna, grid[i, j], []), (i, j))
            end
        end
    end

    antinodes = Set{Tuple{Int,Int}}()
    for (k, v) in antenna
        for i in 1:length(v)
            for j in i+1:length(v)
                push!(antinodes, v[i])
                push!(antinodes, v[j])
                dx = v[j][1] - v[i][1]
                dy = v[j][2] - v[i][2]
                x, y = v[j][1] + dx, v[j][2] + dy
                while 1 <= x <= m && 1 <= y <= n
                    push!(antinodes, (x, y))
                    x, y = x + dx, y + dy
                end
                x, y = v[i][1] - dx, v[i][2] - dy
                while 1 <= x <= m && 1 <= y <= n
                    push!(antinodes, (x, y))
                    x, y = x - dx, y - dy
                end
            end
        end
    end

    return length(antinodes)
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

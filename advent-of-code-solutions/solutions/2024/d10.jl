# 10. https://adventofcode.com/2024/day/10


function part_a(input::AbstractString)
    s = strip(input, '\n')
    grid::Matrix{Int} = stack([parse.(Int, collect(x)) for x in split(s, "\n")], dims=1)
    m, n = size(grid)

    starts = [(i, j) for j in 1:n, i in 1:m if grid[i, j] == 0]
    reachable = Set()
    total = 0
    while !isempty(starts)
        start = popfirst!(starts)
        queue = [[start]]
        while !isempty(queue)
            path = pop!(queue)
            i, j = path[end]
            if grid[i, j] == 9
                if (path[1]..., path[end]...) ∉ reachable
                    push!(reachable, (path[1]..., path[end]...))
                    total += 1
                end
                continue
            end
            for (di, dj) in [(0, 1), (0, -1), (1, 0), (-1, 0)]
                i2, j2 = i + di, j + dj
                if !(1 <= i2 <= m && 1 <= j2 <= n)
                    continue
                end
                value_diff_check = grid[i2, j2] - grid[i, j] == 1
                visited_check = (i2, j2) ∉ path
                if value_diff_check && visited_check
                    push!(queue, vcat(path, [(i2, j2)]))
                end
            end
        end
    end

    return total
end

function part_b(input::AbstractString)
    s = strip(input, '\n')
    grid::Matrix{Int} = stack([parse.(Int, collect(x)) for x in split(s, "\n")], dims=1)
    m, n = size(grid)

    starts = [(i, j) for j in 1:n, i in 1:m if grid[i, j] == 0]
    total = 0
    while !isempty(starts)
        start = popfirst!(starts)
        queue = [[start]]
        while !isempty(queue)
            path = pop!(queue)
            i, j = path[end]
            if grid[i, j] == 9
                total += 1
                continue
            end
            for (di, dj) in [(0, 1), (0, -1), (1, 0), (-1, 0)]
                i2, j2 = i + di, j + dj
                if !(1 <= i2 <= m && 1 <= j2 <= n)
                    continue
                end
                value_diff_check = grid[i2, j2] - grid[i, j] == 1
                visited_check = (i2, j2) ∉ path
                if value_diff_check && visited_check
                    push!(queue, vcat(path, [(i2, j2)]))
                end
            end
        end
    end

    return total
end

test_string_2024_10 = """
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
"""

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

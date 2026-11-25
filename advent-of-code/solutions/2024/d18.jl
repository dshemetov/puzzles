# 18. https://adventofcode.com/2024/day/18


using DataStructures: PriorityQueue, enqueue!, dequeue!

const directions = [CartesianIndex(0, 1), CartesianIndex(1, 0), CartesianIndex(-1, 0), CartesianIndex(0, -1)]

function part_a(input::AbstractString; n=71, m=71, num_bytes=1024)
    s = strip(input, '\n')
    s = split(s, '\n')

    grid::Matrix{Char} = fill('.', n, m)
    for line in s[1:num_bytes]
        y, x = parse.(Int, split(line, ","))
        grid[x+1, y+1] = '#'
    end

    cost, path = solve_maze(grid, n, m)
    return cost
end

function solve_maze(grid::Matrix{Char}, n::Int, m::Int)::Tuple{Int,Vector{CartesianIndex{2}}}
    queue::PriorityQueue{CartesianIndex{2},Int} = PriorityQueue()
    enqueue!(queue, CartesianIndex(1, 1) => 0)

    costs = fill(-1, n, m)
    costs[1, 1] = 0
    came_from = fill(CartesianIndex(-1, -1), n, m)
    came_from[1, 1] = CartesianIndex(-1, -1)

    while !isempty(queue)
        pos = dequeue!(queue)
        cost = costs[pos]
        if pos == CartesianIndex(n, m)
            path = []
            while pos != CartesianIndex(-1, -1)
                push!(path, pos)
                pos = came_from[pos]
            end
            return cost, reverse(path)
        end

        for dir in directions
            pos_ = pos + dir
            if !checkbounds(Bool, grid, pos_) || grid[pos_] == '#'
                continue
            end
            new_cost = cost + 1
            if costs[pos_] == -1 || new_cost < costs[pos_]
                costs[pos_] = new_cost
                enqueue!(queue, pos_ => new_cost)
                came_from[pos_] = pos
            end
        end

    end

    return -1, []
end

function part_b(input::AbstractString; n=71, m=71, num_bytes=1024)
    s = strip(input, '\n')
    s = split(s, '\n')

    grid::Matrix{Char} = fill('.', n, m)
    for line in s[1:num_bytes]
        y, x = parse.(Int, split(line, ","))
        grid[x+1, y+1] = '#'
    end

    i = num_bytes
    cost, path = solve_maze(grid, n, m)
    while cost != -1 && i < length(s)
        i += 1
        y, x = parse.(Int, split(s[i], ","))
        grid[x+1, y+1] = '#'
        if CartesianIndex(x + 1, y + 1) in path
            cost, path = solve_maze(grid, n, m)
        end
    end
    if cost == -1
        return s[i]
    end
    return -1
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

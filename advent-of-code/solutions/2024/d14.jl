# 14. https://adventofcode.com/2024/day/14

function eachmatch_vector(s::AbstractString, regex::Regex)::Vector{String}
    return [m.match for m in eachmatch(regex, s)]
end

function print_grid(grid)
    for row in eachrow(grid)
        println(join(row))
    end
end


function part_a(input::AbstractString; width=101, height=103)
    s = strip(input, '\n')
    digits::Vector{Vector{String}} = [eachmatch_vector(line, r"-?\d+") for line in split(s, '\n')]
    nums::Matrix{Int} = parse.(Int, stack(digits, dims=1))

    for _ in 1:100
        nums[:, 1:2] .= mod.(nums[:, 1:2] .+ nums[:, 3:4], [width height])
    end

    return get_score(nums[:, 1:2], width, height)
end

function part_b(input::AbstractString; width=101, height=103)
    s = strip(input, '\n')
    digits::Vector{Vector{String}} = [eachmatch_vector(line, r"-?\d+") for line in split(s, '\n')]
    nums::Matrix{Int} = parse.(Int, stack(digits, dims=1))

    smallest_score = Inf
    step_of_smallest_score = 0
    for i in 1:10000
        nums[:, 1:2] .= mod.(nums[:, 1:2] .+ nums[:, 3:4], [width height])
        score = check_cluster(nums[:, 1:2], width, height)
        if score < smallest_score
            smallest_score = score
            step_of_smallest_score = i
            # println("New smallest score: $smallest_score at step $step_of_smallest_score")
            # view_robots(pos, width, height)
        end
    end

    return step_of_smallest_score
end

function check_cluster(m::Matrix{Int}, width::Int, height::Int)::Int
    mw = div(width, 2)
    mh = div(height, 2)
    return -sum([1 for i in axes(m, 1) if mw - 5 <= m[i, 1] <= mw + 5 && mh - 5 <= m[i, 2] <= mh + 5], init=0)
end

function get_score(m::Matrix{Int}, width::Int, height::Int)::Int
    quadrants = [0, 0, 0, 0]
    for i in axes(m, 1)
        if m[i, 1] < div(width, 2) && m[i, 2] < div(height, 2)
            quadrants[1] += 1
        elseif m[i, 1] < div(width, 2) && m[i, 2] > div(height, 2)
            quadrants[2] += 1
        elseif m[i, 1] > div(width, 2) && m[i, 2] < div(height, 2)
            quadrants[3] += 1
        elseif m[i, 1] > div(width, 2) && m[i, 2] > div(height, 2)
            quadrants[4] += 1
        end
    end
    return prod(quadrants)
end

function view_robots(m::Matrix{Int}, width::Int, height::Int)
    grid::Matrix{Char} = fill('.', height, width)

    for i in axes(m, 1)
        grid[m[i, 2]+1, m[i, 1]+1] = 'R'
    end

    print_grid(grid)
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

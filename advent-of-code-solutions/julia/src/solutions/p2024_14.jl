"""14. https://adventofcode.com/2024/day/14"""

function solve(input::Question{2024,14,'a'})
    if input.s == ""
        s = strip(test_string_2024_14, '\n')
        width = 11
        height = 7
    else
        s = strip(input.s, '\n')
        width = 101
        height = 103
    end
    digits::Vector{Vector{String}} = [eachmatch_vector(line, r"-?\d+") for line in split(s, '\n')]
    nums::Matrix{Int} = parse.(Int, stack(digits, dims=1))

    for _ in 1:100
        nums[:, 1:2] .= mod.(nums[:, 1:2] .+ nums[:, 3:4], [width height])
    end

    return get_score(nums[:, 1:2], width, height)
end

function solve(input::Question{2024,14,'b'})
    if input.s == ""
        s = strip(test_string_2024_14, '\n')
        width = 11
        height = 7
    else
        s = strip(input.s, '\n')
        width = 101
        height = 103
    end
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

test_string_2024_14 = """
p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3
"""


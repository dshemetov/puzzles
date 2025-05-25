"""14. https://adventofcode.com/2024/day/14"""

function solve(input::Question{2024,14,'a'})
    if input.s == ""
        s = test_string_2024_14
        width = 11
        height = 7
    else
        s = input.s
        width = 101
        height = 103
    end
    s = strip(s, '\n')
    nums = [parse.(Int, eachmatch_vector(line, r"-?\d+")) for line in split(s, '\n')]
    pos = hcat([[n[1], n[2]] for n in nums]...)'  # m x 2 matrix of positions
    vel = hcat([[n[3], n[4]] for n in nums]...)'  # m x 2 matrix of velocities

    for _ in 1:100
        pos .= mod.(pos .+ vel, [width height])
    end

    return get_score(pos, width, height)
end

function solve(input::Question{2024,14,'b'})
    if input.s == ""
        s = test_string_2024_14
        width = 11
        height = 7
    else
        s = input.s
        width = 101
        height = 103
    end
    s = strip(s, '\n')
    nums = [parse.(Int, eachmatch_vector(line, r"-?\d+")) for line in split(s, '\n')]
    pos = hcat([[n[1], n[2]] for n in nums]...)'  # m x 2 matrix of positions
    vel = hcat([[n[3], n[4]] for n in nums]...)'  # m x 2 matrix of velocities

    smallest_score = Inf
    step_of_smallest_score = 0
    for i in 1:10000
        pos .= mod.(pos .+ vel, [width height])
        score = check_cluster(pos, width, height)
        if score < smallest_score
            smallest_score = score
            step_of_smallest_score = i
            # println("New smallest score: $smallest_score at step $step_of_smallest_score")
            # view_robots(pos, width, height)
        end
    end

    return step_of_smallest_score
end

function check_cluster(pos, width, height)
    mw = div(width, 2)
    mh = div(height, 2)
    return -sum([1 for i in axes(pos, 1) if mw - 5 <= pos[i, 1] <= mw + 5 && mh - 5 <= pos[i, 2] <= mh + 5], init=0)
end

function get_score(pos, width, height)
    quadrants = [0, 0, 0, 0]
    for i in axes(pos, 1)
        if pos[i, 1] < div(width, 2) && pos[i, 2] < div(height, 2)
            quadrants[1] += 1
        elseif pos[i, 1] < div(width, 2) && pos[i, 2] > div(height, 2)
            quadrants[2] += 1
        elseif pos[i, 1] > div(width, 2) && pos[i, 2] < div(height, 2)
            quadrants[3] += 1
        elseif pos[i, 1] > div(width, 2) && pos[i, 2] > div(height, 2)
            quadrants[4] += 1
        end
    end
    return prod(quadrants)
end

function view_robots(pos, width, height)
    grid = fill('.', height, width)

    for i in axes(pos, 1)
        grid[pos[i, 2]+1, pos[i, 1]+1] = 'R'
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


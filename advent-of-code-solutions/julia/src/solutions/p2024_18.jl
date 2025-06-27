"""18. https://adventofcode.com/2024/day/18"""

const directions = [CartesianIndex(0, 1), CartesianIndex(1, 0), CartesianIndex(-1, 0), CartesianIndex(0, -1)]

function solve(input::Question{2024,18,'a'})
    if input.s == ""
        n, m = 7, 7
        num_bytes = 12
        s = strip(test_string_2024_18, '\n')
    else
        n, m = 71, 71
        num_bytes = 1024
        s = strip(input.s, '\n')
    end
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

function solve(input::Question{2024,18,'b'})
    if input.s == ""
        n, m = 7, 7
        num_bytes = 12
        s = strip(test_string_2024_18, '\n')
    else
        n, m = 71, 71
        num_bytes = 1024
        s = strip(input.s, '\n')
    end
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

test_string_2024_18 = """
5,4
4,2
4,5
3,0
2,1
6,3
2,4
1,5
0,6
3,3
2,6
5,1
1,2
5,5
2,5
6,5
1,4
0,4
6,4
1,1
6,1
1,0
0,5
1,6
2,0
"""

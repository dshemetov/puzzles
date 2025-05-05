function solve(input::Question{2024,18,'a'})
    if input.s == ""
        n, m = 7, 7
        num_bytes = 12
        s = test_string_2024_18
    else
        n, m = 71, 71
        num_bytes = 1024
        s = input.s
    end
    s = strip(s, '\n')
    s = split(s, '\n')

    grid = fill('.', n, m)
    for line in s[1:num_bytes]
        y, x = parse.(Int, split(line, ","))
        grid[x+1, y+1] = '#'
    end

    cost, path = solve_maze(grid, n, m)
    return cost
end

function solve_maze(grid, n, m)
    # Now we have to do a maze solve
    queue = PriorityQueue()
    enqueue!(queue, (1, 1) => 0)

    costs = Dict{Tuple{Int,Int},Int}()
    costs[(1, 1)] = 0
    came_from = Dict{Tuple{Int,Int},Tuple{Int,Int}}()
    came_from[(1, 1)] = (-1, -1)

    while !isempty(queue)
        pos = dequeue!(queue)
        cost = costs[pos]
        if pos == (n, m)
            path = []
            while pos != (-1, -1)
                push!(path, pos)
                pos = came_from[pos]
            end
            return cost, reverse(path)
        end

        for dir in [(0, 1), (1, 0), (-1, 0), (0, -1)]
            x, y = pos .+ dir
            if !(1 <= x <= n && 1 <= y <= m) || grid[x, y] == '#'
                continue
            end
            new_cost = cost + 1
            if !haskey(costs, (x, y)) || new_cost < costs[(x, y)]
                costs[(x, y)] = new_cost
                enqueue!(queue, (x, y) => new_cost)
                came_from[(x, y)] = pos
            end
        end

    end

    return -1, []
end

function solve(input::Question{2024,18,'b'})
    if input.s == ""
        n, m = 7, 7
        num_bytes = 12
        s = test_string_2024_18
    else
        n, m = 71, 71
        num_bytes = 1024
        s = input.s
    end
    s = strip(s, '\n')
    s = split(s, '\n')

    grid = fill('.', n, m)
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
        if (x + 1, y + 1) in path
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

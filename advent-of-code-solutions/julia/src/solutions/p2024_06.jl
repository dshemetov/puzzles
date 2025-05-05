function solve(input::Question{2024,6,'a'})
    if input.s == ""
        s = test_string_2024_06
    else
        s = input.s
    end
    s = strip(s, '\n')
    grid = stack([collect(row) for row in split(s, '\n')], dims=1)
    m, n = size(grid)

    # Find start position
    pos = collect(Tuple(findfirst(==('^'), grid)))
    grid[pos[1], pos[2]] = '.'

    turn_map = Dict{Vector{Int},Vector{Int}}(
        [-1, 0] => [0, 1],
        [0, 1] => [1, 0],
        [1, 0] => [0, -1],
        [0, -1] => [-1, 0]
    )
    visited = Set{Vector{Int}}([pos])
    d = [-1, 0]
    while 1 <= pos[1] <= m && 1 <= pos[2] <= n
        if grid[pos[1], pos[2]] == '#'
            pos = pos - d
            d = turn_map[d]
        else
            push!(visited, pos)
        end
        pos = pos + d
    end
    return length(visited)
end

function solve(input::Question{2024,6,'b'})
    if input.s == ""
        s = test_string_2024_06
    else
        s = input.s
    end
    s = strip(s, '\n')
    grid = stack([collect(row) for row in split(s, '\n')], dims=1)
    m, n = size(grid)

    # Find start position
    start_pos = collect(Tuple(findfirst(==('^'), grid)))
    grid[start_pos[1], start_pos[2]] = '.'

    pos = start_pos
    turn_map = Dict{Vector{Int},Vector{Int}}(
        [-1, 0] => [0, 1],
        [0, 1] => [1, 0],
        [1, 0] => [0, -1],
        [0, -1] => [-1, 0]
    )
    visited = Set{Vector{Int}}([pos])
    d = [-1, 0]
    while 1 <= pos[1] <= m && 1 <= pos[2] <= n
        if grid[pos[1], pos[2]] == '#'
            pos = pos - d
            d = turn_map[d]
        else
            push!(visited, pos)
        end
        pos = pos + d
    end
    delete!(visited, pos)

    # Compress the grid to just the obstacles
    obstacles = Set([[i, j] for i in 1:m for j in 1:n if grid[i, j] == '#'])
    xs = [sort([x for x in obstacles if x[2] == j], by=x -> x[1]) for j in 1:n]
    ys = [sort([x for x in obstacles if x[1] == i], by=x -> x[2]) for i in 1:m]

    function get_next_obstacle(pos::Vector{Int}, d::Vector{Int})
        row, col = pos
        if d == [-1, 0]
            idx = bisect_left(xs[col], pos, key=x -> x[1])
            if idx >= 1
                obstacle = xs[col][idx]
                return (obstacle - d, obstacle, [0, 1])
            end
        elseif d == [0, 1]
            idx = bisect_right(ys[row], pos, key=x -> x[2])
            if idx <= length(ys[row])
                obstacle = ys[row][idx]
                return (obstacle - d, obstacle, [1, 0])
            end
        elseif d == [1, 0]
            idx = bisect_right(xs[col], pos, key=x -> x[1])
            if idx <= length(xs[col])
                obstacle = xs[col][idx]
                return (obstacle - d, obstacle, [0, -1])
            end
        elseif d == [0, -1]
            idx = bisect_left(ys[row], pos, key=x -> x[2])
            if idx >= 1
                obstacle = ys[row][idx]
                return (obstacle - d, obstacle, [-1, 0])
            end
        end
        return nothing, nothing, nothing
    end

    total = 0
    for change_pos in visited
        if grid[change_pos[1], change_pos[2]] == "#"
            continue
        end

        d = [-1, 0]
        push!(obstacles, change_pos)
        insort!(xs[change_pos[2]], change_pos, key=x -> x[1])
        insort!(ys[change_pos[1]], change_pos, key=y -> y[2])

        pos, obstacle, d = get_next_obstacle(start_pos, d)
        visited_obstacles = Set{Tuple{Vector{Int},Vector{Int}}}()
        while !isnothing(pos) && !((pos, obstacle) in visited_obstacles)
            push!(visited_obstacles, (pos, obstacle))
            pos, obstacle, d = get_next_obstacle(pos, d)
        end
        if !isnothing(pos) && (pos, obstacle) in visited_obstacles
            total += 1
        end
        delete!(obstacles, change_pos)
        deleteat!(xs[change_pos[2]], findfirst(==(change_pos), xs[change_pos[2]]))
        deleteat!(ys[change_pos[1]], findfirst(==(change_pos), ys[change_pos[1]]))
    end

    return total

end

test_string_2024_06 = """
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
"""

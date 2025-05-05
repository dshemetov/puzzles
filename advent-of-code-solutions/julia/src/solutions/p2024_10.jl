function solve(input::Question{2024,10,'a'})
    if input.s == ""
        s = test_string_2024_10
    else
        s = input.s
    end
    s = strip(s, '\n')
    grid = string_to_matrix(s)
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

function solve(input::Question{2024,10,'b'})
    if input.s == ""
        s = test_string_2024_10
    else
        s = input.s
    end
    s = strip(s, '\n')
    grid = string_to_matrix(s)
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

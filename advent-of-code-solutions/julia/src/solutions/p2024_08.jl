function solve(input::Question{2024,8,'a'})
    if input.s == ""
        s = test_string_2024_8
    else
        s = input.s
    end
    s = strip(s, '\n')
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

function solve(input::Question{2024,8,'b'})
    if input.s == ""
        s = test_string_2024_8
    else
        s = input.s
    end
    s = strip(s, '\n')
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

test_string_2024_8 = """
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
"""

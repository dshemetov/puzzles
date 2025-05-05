function solve(input::Question{2024,12,'a'})
    if input.s == ""
        s = split(test_string_2024_12, "\n\n")[2]
    else
        s = input.s
    end
    s = strip(s, '\n')
    grid = [collect(row) for row in split(s, '\n')]
    m, n = length(grid), length(grid[1])
    visited = Set{Tuple{Int,Int}}()

    function get_region(i, j)
        region = []
        t = grid[i][j]
        stack = [(i, j)]
        while !isempty(stack)
            i, j = pop!(stack)
            if !(1 <= i <= m && 1 <= j <= n && grid[i][j] == t && (i, j) ∉ visited)
                continue
            end
            push!(region, (i, j))
            push!(visited, (i, j))
            push!(stack, (i - 1, j))
            push!(stack, (i + 1, j))
            push!(stack, (i, j - 1))
            push!(stack, (i, j + 1))
        end
        return region
    end
    regions = [get_region(i, j) for i in 1:m, j in 1:n if (i, j) ∉ visited]

    directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
    perimeters = [sum(1 for p in region for d in directions if p .+ d ∉ region) for region in regions]
    return sum(length.(regions) .* perimeters)
end

function solve(input::Question{2024,12,'b'})
    if input.s == ""
        s = split(test_string_2024_12, "\n\n")[4]
    else
        s = input.s
    end
    s = strip(s, '\n')
    grid = [collect(row) for row in split(s, '\n')]
    m, n = length(grid), length(grid[1])
    visited = Set{Tuple{Int,Int}}()

    function get_region(i::Int, j::Int)::Vector{Tuple{Int,Int}}
        region = []
        t = grid[i][j]
        stack = [(i, j)]
        while !isempty(stack)
            i, j = pop!(stack)
            if !(1 <= i <= m && 1 <= j <= n && grid[i][j] == t && (i, j) ∉ visited)
                continue
            end
            push!(region, (i, j))
            push!(visited, (i, j))
            push!(stack, (i - 1, j))
            push!(stack, (i + 1, j))
            push!(stack, (i, j - 1))
            push!(stack, (i, j + 1))
        end
        return region
    end
    regions = [get_region(i, j) for i in 1:m, j in 1:n if (i, j) ∉ visited]

    sides = [count_sides(region) for region in regions]
    return sum(length.(regions) .* sides)
end

test_string_2024_12 = """
AAAA
BBCD
BBCC
EEEC

RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE

EEEEE
EXXXX
EEEEE
EXXXX
EEEEE

AAAAAA
AAABBA
AAABBA
ABBAAA
ABBAAA
AAAAAA
"""

function count_sides(points::Vector{Tuple{Int,Int}})
    points = Set(points)

    # Define the common corner directions once
    corner_directions = [
        ((1, 0), (1, 1), (0, 1)),    # right-down
        ((1, 0), (1, -1), (0, -1)),  # left-down
        ((-1, 0), (-1, 1), (0, 1)),  # right-up
        ((-1, 0), (-1, -1), (0, -1)) # left-up
    ]

    # Define patterns for different corner types
    corner_patterns = [
        (false, false, false),  # Exterior corners
        (true, false, true),    # Interior corners
        (false, true, false)    # Corner points touching
    ]

    return sum(
        [point .+ d in points for d in directions] == collect(pattern)
        for point in points,
        pattern in corner_patterns,
        directions in corner_directions
    )
end

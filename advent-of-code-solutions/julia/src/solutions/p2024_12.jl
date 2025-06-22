"""12. https://adventofcode.com/2024/day/12"""

function solve(input::Question{2024,12,'a'})
    if input.s == ""
        s = strip(split(test_string_2024_12, "\n\n")[2], '\n')
    else
        s = strip(input.s, '\n')
    end

    lines = split(s, '\n')
    m, n = length(lines), length(lines[1])

    grid = Matrix{UInt8}(undef, m, n)
    for (i, line) in enumerate(lines)
        for (j, char) in enumerate(line)
            grid[i, j] = UInt8(char)
        end
    end

    visited = falses(m, n)
    total::Int = 0

    # Pre-allocate region vector to avoid repeated allocations
    region = Vector{Tuple{Int,Int}}()

    for i in 1:m, j in 1:n
        if visited[i, j]
            continue
        end

        # Clear and reuse the region vector
        empty!(region)

        # DFS to find connected region
        char_type = grid[i, j]
        stack = [(i, j)]

        while !isempty(stack)
            ci, cj = pop!(stack)
            if ci < 1 || ci > m || cj < 1 || cj > n || visited[ci, cj] || grid[ci, cj] != char_type
                continue
            end

            visited[ci, cj] = true
            push!(region, (ci, cj))

            # Add neighbors
            push!(stack, (ci - 1, cj))
            push!(stack, (ci + 1, cj))
            push!(stack, (ci, cj - 1))
            push!(stack, (ci, cj + 1))
        end

        if isempty(region)
            continue
        end

        # Calculate perimeter efficiently
        area = length(region)
        perimeter = 0

        for (ri, rj) in region
            # Check each direction
            for (di, dj) in ((-1, 0), (1, 0), (0, -1), (0, 1))
                ni, nj = ri + di, rj + dj
                # Count edge if neighbor is out of bounds or different type
                if ni < 1 || ni > m || nj < 1 || nj > n || grid[ni, nj] != char_type
                    perimeter += 1
                end
            end
        end

        total += area * perimeter
    end

    return total
end

function solve(input::Question{2024,12,'b'})
    if input.s == ""
        s = strip(split(test_string_2024_12, "\n\n")[4], '\n')
    else
        s = strip(input.s, '\n')
    end

    lines = split(s, '\n')
    m, n = length(lines), length(lines[1])

    # Use a more efficient grid representation
    grid = Matrix{UInt8}(undef, m, n)
    for (i, line) in enumerate(lines)
        for (j, char) in enumerate(line)
            grid[i, j] = UInt8(char)
        end
    end

    visited = falses(m, n)
    total::Int = 0

    # Pre-allocate region vector to avoid repeated allocations
    region = Vector{Tuple{Int,Int}}()

    for i in 1:m, j in 1:n
        if visited[i, j]
            continue
        end

        # Clear and reuse the region vector
        empty!(region)

        # DFS to find connected region
        char_type = grid[i, j]
        stack = [(i, j)]

        while !isempty(stack)
            ci, cj = pop!(stack)
            if ci < 1 || ci > m || cj < 1 || cj > n || visited[ci, cj] || grid[ci, cj] != char_type
                continue
            end

            visited[ci, cj] = true
            push!(region, (ci, cj))

            # Add neighbors
            push!(stack, (ci - 1, cj))
            push!(stack, (ci + 1, cj))
            push!(stack, (ci, cj - 1))
            push!(stack, (ci, cj + 1))
        end

        if isempty(region)
            continue
        end

        # Calculate sides efficiently
        area = length(region)
        sides = count_sides(region)

        total += area * sides
    end

    return total
end

function count_sides(region::Vector{Tuple{Int,Int}})::Int
    # Convert region to a set for O(1) lookups
    region_set = Set(region)

    # Define the common corner directions
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

    total_sides = 0

    for (i, j) in region
        for directions in corner_directions
            for pattern in corner_patterns
                # Check if this corner configuration matches the pattern
                matches = true
                for (k, (di, dj)) in enumerate(directions)
                    ni, nj = i + di, j + dj
                    in_region = (ni, nj) in region_set
                    if in_region != pattern[k]
                        matches = false
                        break
                    end
                end

                if matches
                    total_sides += 1
                end
            end
        end
    end

    return total_sides
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

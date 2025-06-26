"""6. https://adventofcode.com/2024/day/6"""

# Direction constants: up=1, right=2, down=3, left=4
const DIRECTIONS = (CartesianIndex(-1, 0), CartesianIndex(0, 1), CartesianIndex(1, 0), CartesianIndex(0, -1))
# Turn right: up->right, right->down, down->left, left->up
const TURN_RIGHT = (2, 3, 4, 1)

function solve(input::Question{2024,6,'a'})
    if input.s == ""
        s = strip(test_string_2024_06, '\n')
    else
        s = strip(input.s, '\n')
    end
    grid::Matrix{Char} = stack(split(s, "\n")) |> permutedims
    m::Int, n::Int = size(grid)
    start_pos::CartesianIndex{2} = findfirst(==('^'), grid)
    grid[start_pos] = '.'

    visited::BitMatrix = falses(m, n)
    pos::CartesianIndex{2} = start_pos
    dir::Int = 1  # Start facing up
    total::Int = 0
    while checkbounds(Bool, grid, pos)
        if grid[pos] == '#'
            # Back up and turn right
            pos = pos - DIRECTIONS[dir]
            dir = TURN_RIGHT[dir]
        else
            if !visited[pos]
                visited[pos] = true
                total += 1
            end
            pos = pos + DIRECTIONS[dir]
        end
    end
    return total
end

function solve(input::Question{2024,6,'b'})
    if input.s == ""
        s = strip(test_string_2024_06, '\n')
    else
        s = strip(input.s, '\n')
    end
    grid::Matrix{Char} = stack(split(s, "\n")) |> permutedims
    m::Int, n::Int = size(grid)
    start_pos::CartesianIndex{2} = findfirst(==('^'), grid)
    grid[start_pos] = '.'

    # Get original path
    original_path::Vector{CartesianIndex{2}} = get_path(grid, start_pos, m, n)

    # Pre-allocate reusable BitArray
    visited_states::BitArray{3} = falses(m, n, 4)

    # Try placing an obstacle in each position on the original path
    total::Int = 0
    for test_pos in original_path
        if grid[test_pos] == '#' || test_pos == start_pos
            continue
        end
        # If the obstacle creates a loop, it's a valid obstacle
        if creates_loop(grid, start_pos, test_pos, visited_states)
            total += 1
        end
    end
    return total
end

function get_path(grid::Matrix{Char}, start_pos::CartesianIndex{2}, m::Int, n::Int)::Vector{CartesianIndex{2}}
    visited::BitMatrix = falses(m, n)
    path::Vector{CartesianIndex{2}} = CartesianIndex{2}[]
    pos::CartesianIndex{2} = start_pos
    dir::Int = 1  # Start facing up
    while checkbounds(Bool, grid, pos)
        if grid[pos] == '#'
            # Back up and turn right
            pos = pos - DIRECTIONS[dir]
            dir = TURN_RIGHT[dir]
        else
            if !visited[pos]
                visited[pos] = true
                push!(path, pos)
            end
        end
        pos = pos + DIRECTIONS[dir]
    end
    return path
end

function creates_loop(
    grid::Matrix{Char},
    start_pos::CartesianIndex{2},
    obstacle_pos::CartesianIndex{2},
    visited_states::BitArray{3}
)::Bool
    # Efficiently clear the BitArray instead of allocating new one
    fill!(visited_states, false)

    # Temporarily add obstacle
    original_char::Char = grid[obstacle_pos]
    grid[obstacle_pos] = '#'

    pos::CartesianIndex{2} = start_pos
    dir::Int = 1
    result::Bool = false

    while checkbounds(Bool, grid, pos)
        if visited_states[pos, dir]
            result = true
            break
        end

        visited_states[pos, dir] = true
        next_pos = pos + DIRECTIONS[dir]

        if checkbounds(Bool, grid, next_pos) && grid[next_pos] == '#'
            dir = TURN_RIGHT[dir]
        else
            pos = next_pos
        end
    end

    # Clean up
    grid[obstacle_pos] = original_char
    return result
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

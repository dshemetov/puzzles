"""4. https://adventofcode.com/2024/day/4"""


function solve(input::Question{2024,4,'a'})
    if input.s == ""
        s = strip(test_string_2024_04, '\n')
    else
        s = strip(input.s, '\n')
    end
    grid::Matrix{Char} = stack(split(s, "\n"))

    total::Int = 0
    directions::NTuple{4,CartesianIndex{2}} = (CartesianIndex(0, 1), CartesianIndex(1, 0), CartesianIndex(1, 1), CartesianIndex(-1, 1))
    for pos::CartesianIndex{2} in eachindex(IndexCartesian(), grid), d in directions, sgn in [1, -1]
        valid::Bool = true
        for k in 1:4
            if !checkbounds(Bool, grid, pos + sgn * (k - 1) * d)
                valid = false
                break
            end
        end
        if !valid
            continue
        end
        if grid[pos] == 'X' && grid[pos+sgn*d] == 'M' && grid[pos+sgn*2*d] == 'A' && grid[pos+sgn*3*d] == 'S'
            total += 1
        end
    end
    return total
end

function solve(input::Question{2024,4,'b'})
    if input.s == ""
        s = strip(test_string_2024_04, '\n')
    else
        s = strip(input.s, '\n')
    end
    grid::Matrix{Char} = stack(split(s, "\n"))

    d1 = CartesianIndex(-1, 1)
    d2 = CartesianIndex(-1, -1)
    total::Int = 0
    for pos::CartesianIndex{2} in eachindex(IndexCartesian(), grid)
        # Ignore positions on edges.
        if pos[1] == 1 || pos[1] == size(grid, 1) || pos[2] == 1 || pos[2] == size(grid, 2)
            continue
        end
        # Check for MAS and SAM patterns.
        one = grid[pos-d1] == 'M' && grid[pos] == 'A' && grid[pos+d1] == 'S'
        two = grid[pos-d1] == 'S' && grid[pos] == 'A' && grid[pos+d1] == 'M'
        three = grid[pos-d2] == 'M' && grid[pos] == 'A' && grid[pos+d2] == 'S'
        four = grid[pos-d2] == 'S' && grid[pos] == 'A' && grid[pos+d2] == 'M'
        if (one || two) && (three || four)
            total += 1
        end
    end
    return total
end

test_string_2024_04 = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

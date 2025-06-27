"""25. https://adventofcode.com/2024/day/25"""

function solve(input::Question{2024,25,'a'})
    if input.s == ""
        s = strip(test_string_2024_25, '\n')
    else
        s = strip(input.s, '\n')
    end

    schematics = split(s, "\n\n")
    locks = Vector{Int}[]
    keys = Vector{Int}[]
    for schematic in schematics
        grid::Matrix{Char} = stack(split(schematic, "\n"), dims=1)
        if grid[1, 1] == '#'
            push!(locks, [findfirst(==('.'), grid[:, i]) - 2 for i in axes(grid, 2)])
        else
            push!(keys, [findfirst(==('.'), reverse(grid[:, i])) - 2 for i in axes(grid, 2)])
        end
    end
    total = 0
    for lock in locks
        for key in keys
            if all(lock .+ key .<= 5)
                total += 1
            end
        end
    end
    return total
end

function solve(input::Question{2024,25,'b'})
    if input.s == ""
        s = strip(test_string_2024_25, '\n')
    else
        s = strip(input.s, '\n')
    end
    return 0
end

test_string_2024_25 = """
#####
.####
.####
.####
.#.#.
.#...
.....

#####
##.##
.#.##
...##
...#.
...#.
.....

.....
#....
#....
#...#
#.#.#
#.###
#####

.....
.....
#.#..
###..
###.#
###.#
#####

.....
.....
.....
#....
#.#..
#.#.#
#####
"""
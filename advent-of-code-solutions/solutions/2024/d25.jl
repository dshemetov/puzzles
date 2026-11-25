# 25. https://adventofcode.com/2024/day/25


function part_a(input::AbstractString)
    s = strip(input, '\n')

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

function part_b(input::AbstractString)
    s = strip(input, '\n')
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

function main(path)
    input = read(path, String)
    for (name, part) in (("part_a", part_a), ("part_b", part_b))
        first_call = @elapsed answer = part(input)
        println(answer)
        # The first call includes compiling. Call again (if it was quick) to time just the work.
        warm = first_call < 2 ? @elapsed(part(input)) : first_call
        println(stderr, name, ": ", round(warm, digits=4), "s (first call ", round(first_call, digits=4), "s)")
    end
end

# Only runs as a script, so `include`-ing this file in a REPL stays quiet.
if abspath(PROGRAM_FILE) == @__FILE__
    main(ARGS[1])
end

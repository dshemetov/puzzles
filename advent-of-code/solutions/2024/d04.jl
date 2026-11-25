# 4. https://adventofcode.com/2024/day/4


function part_a(input::AbstractString)
    s = strip(input, '\n')
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

function part_b(input::AbstractString)
    s = strip(input, '\n')
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

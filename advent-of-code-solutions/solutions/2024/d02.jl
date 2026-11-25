# 2. https://adventofcode.com/2024/day/2
# Alternative approach: d02-vectorized.jl

function part_a(input::AbstractString)
    s = strip(input, '\n')
    lines::Vector{Vector{Int}} = [parse.(Int, split(line, " ")) for line in split(s, "\n")]
    total::Int = 0
    for line in lines
        all_increasing::Bool = true
        all_decreasing::Bool = true
        changes_bounded::Bool = true
        for i = 1:length(line)-1
            all_increasing &= line[i] < line[i+1]
            all_decreasing &= line[i] > line[i+1]
            changes_bounded &= 1 <= abs(line[i] - line[i+1]) <= 3
            if !(all_increasing || all_decreasing) || !changes_bounded
                break
            end
        end
        total += (all_increasing || all_decreasing) && changes_bounded
    end
    return total
end

function part_b(s::AbstractString)
    lines::Vector{Vector{Int}} = [parse.(Int, split(line, " ")) for line in split(strip(s, '\n'), "\n")]
    total::Int = 0
    for line in lines
        all_increasing::Bool = true
        all_decreasing::Bool = true
        changes_bounded::Bool = true
        retry::Bool = false
        for i = 1:length(line)-1
            all_increasing &= line[i] < line[i+1]
            all_decreasing &= line[i] > line[i+1]
            changes_bounded &= 1 <= abs(line[i] - line[i+1]) <= 3
            if !(all_increasing || all_decreasing) || !changes_bounded
                retry = true
                break
            end
        end
        if retry
            retry_success::Bool = false
            for j = 1:length(line)
                new_line = vcat(line[1:j-1], line[j+1:end])
                all_increasing = true
                all_decreasing = true
                changes_bounded = true
                for i = 1:length(new_line)-1
                    all_increasing &= new_line[i] < new_line[i+1]
                    all_decreasing &= new_line[i] > new_line[i+1]
                    changes_bounded &= 1 <= abs(new_line[i] - new_line[i+1]) <= 3
                    if !(all_increasing || all_decreasing) || !changes_bounded
                        break
                    end
                end
                if (all_increasing || all_decreasing) && changes_bounded
                    retry_success = true
                    break
                end
            end
        end
        total += (all_increasing || all_decreasing) && changes_bounded || retry_success
    end
    return total
end

# Example usage
test_string_2024_02 = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
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

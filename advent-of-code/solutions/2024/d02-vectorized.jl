# 2. https://adventofcode.com/2024/day/2
# Variant of d02.jl: part b with vectorized diffs (same answers, different approach).

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
    diffs::Vector{Vector{Int}} = [diff(line) for line in lines]
    all_increasing = Bool[all(diff .>= 0) for diff in diffs]
    all_decreasing = Bool[all(diff .<= 0) for diff in diffs]
    changes_bounded = Bool[all(1 .<= abs.(diff) .<= 3) for diff in diffs]
    valid_vector = vec((all_increasing .| all_decreasing) .& changes_bounded)
    bad_lines = lines[.!valid_vector]
    total = sum(valid_vector)
    for line in bad_lines
        for i in 1:length(line)
            new_line = vcat(line[1:i-1], line[i+1:end])
            diffs_new = diff(new_line)
            all_increasing_new::Bool = all(diffs_new .>= 0)
            all_decreasing_new::Bool = all(diffs_new .<= 0)
            changes_bounded_new::Bool = all(1 .<= abs.(diffs_new) .<= 3)
            if (all_increasing_new || all_decreasing_new) && changes_bounded_new
                total += 1
                break
            end
        end
    end
    return total
end

# Example usage

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

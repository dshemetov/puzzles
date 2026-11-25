# 3. https://adventofcode.com/2024/day/3


function part_a(input::AbstractString)
    s = strip(input, '\n')
    digits::Vector{Vector{String}} = [[x[1], x[2]] for x in eachmatch(r"mul\((\d+),(\d+)\)", s)]
    m::Matrix{Int} = parse.(Int, stack(digits, dims=1))
    return sum(m[:, 1] .* m[:, 2])
end

function part_b(input::AbstractString)
    s = strip(input, '\n')
    doflags::Vector{Int} = vcat([1], [x.offset for x in eachmatch(r"do\(\)", s)])
    dontflags::Vector{Int} = [x.offset for x in eachmatch(r"don't\(\)", s)]
    active_ranges::Vector{Tuple{Int,Int}} = []
    hi::Int = 1
    for start in doflags
        if !isempty(active_ranges) && (last(active_ranges)[1] <= start <= last(active_ranges)[2])
            continue
        end
        while hi <= length(dontflags) && dontflags[hi] < start
            hi += 1
        end
        if hi <= length(dontflags)
            push!(active_ranges, (start, dontflags[hi]))
        else
            push!(active_ranges, (start, length(s)))
            break
        end
    end

    valid_substrings::Vector{String} = [s[i:j] for (i, j) in active_ranges]
    values::Vector{Vector{String}} = [[x[1], x[2]] for vs in valid_substrings for x in eachmatch(r"mul\((\d+),(\d+)\)", vs)]
    m::Matrix{Int} = stack([parse.(Int, pair) for pair in values], dims=1)
    return sum(m[:, 1] .* m[:, 2])
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

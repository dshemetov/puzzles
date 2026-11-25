# 11. https://adventofcode.com/2024/day/11


function transform_int(n::Int)::Vector{Int}
    if n == 0
        return [1]
    end

    digits = ndigits(n)
    if digits % 2 == 0
        divisor = 10^(digits ÷ 2)
        left = n ÷ divisor
        right = n % divisor
        return [left, right]
    else
        return [n * 2024]
    end
end

function part_a(input::AbstractString)
    s = strip(input, '\n')

    # Use integers directly instead of strings
    counts::Dict{Int,Int} = Dict(parse(Int, x) => 1 for x in split(s))

    for _ in 1:25
        new_counts::Dict{Int,Int} = Dict{Int,Int}()
        for (num, count) in counts
            for new_num in transform_int(num)
                new_counts[new_num] = get(new_counts, new_num, 0) + count
            end
        end
        counts = new_counts
    end

    return sum(values(counts))
end

function part_b(input::AbstractString)
    s = strip(input, '\n')

    # Use integers directly instead of strings
    counts::Dict{Int,Int} = Dict(parse(Int, x) => 1 for x in split(s))

    for _ in 1:75
        new_counts::Dict{Int,Int} = Dict{Int,Int}()
        for (num, count) in counts
            for new_num in transform_int(num)
                new_counts[new_num] = get(new_counts, new_num, 0) + count
            end
        end
        counts = new_counts
    end

    return sum(values(counts))
end

test_string_2024_11 = """
125 17
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

# 1. https://adventofcode.com/2024/day/1


function part_a(input::AbstractString)
    s = strip(input, '\n')
    m::Matrix{Int} = parse.(Int, stack([split(x) for x in split(s, "\n")], dims=1))
    m[:, 1] = sort(m[:, 1])
    m[:, 2] = sort(m[:, 2])
    sum(abs.(m[:, 1] - m[:, 2]))
end

function part_b(input::AbstractString)
    s = strip(input, '\n')
    m::Matrix{Int} = parse.(Int, stack([split(x) for x in split(s, "\n")], dims=1))
    c = zeros(Int, maximum(m))
    for x in m[:, 2]
        c[x] += 1
    end
    sum(abs.(x * c[x] for x in m[:, 1]))
end

test_string_2024_01 = """
3   4
4   3
2   5
1   3
3   9
3   3
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

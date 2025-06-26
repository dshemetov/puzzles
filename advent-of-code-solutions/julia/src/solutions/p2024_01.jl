"""1. https://adventofcode.com/2024/day/1"""

function solve(input::Question{2024,1,'a'})
    if input.s == ""
        s = strip(test_string_2024_01, '\n')
    else
        s = strip(input.s, '\n')
    end
    m::Matrix{Int} = parse.(Int, stack([split(x) for x in split(s, "\n")], dims=1))
    m[:, 1] = sort(m[:, 1])
    m[:, 2] = sort(m[:, 2])
    sum(abs.(m[:, 1] - m[:, 2]))
end

function solve(input::Question{2024,1,'b'})
    if input.s == ""
        s = strip(test_string_2024_01, '\n')
    else
        s = strip(input.s, '\n')
    end
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

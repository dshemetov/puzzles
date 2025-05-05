"""1. https://adventofcode.com/2024/day/1"""

function solve(input::Question{2024,1,'a'})
    if input.s == ""
        s = test_string_2024_01
    else
        s = input.s
    end
    s = strip(s, '\n')
    m = string_to_matrix(s, "")
    m[:, 1] = sort(m[:, 1])
    m[:, 2] = sort(m[:, 2])
    sum(abs.(m[:, 1] - m[:, 2]))
end

function Counter(a::AbstractArray)
    Dict(x => count(e -> e == x, a) for x in unique(a))
end

function solve(input::Question{2024,1,'b'})
    if input.s == ""
        s = test_string_2024_01
    else
        s = input.s
    end
    s = strip(s, '\n')
    m = string_to_matrix(s, "")
    c = Counter(m[:, 2])
    sum(abs.(x * get!(c, x, 0) for x in m[:, 1]))
end

test_string_2024_01 = """
3   4
4   3
2   5
1   3
3   9
3   3
"""

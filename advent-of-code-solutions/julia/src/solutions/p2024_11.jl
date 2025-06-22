"""11. https://adventofcode.com/2024/day/11"""

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

function solve(input::Question{2024,11,'a'})
    if input.s == ""
        s = strip(test_string_2024_11, '\n')
    else
        s = strip(input.s, '\n')
    end

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

function solve(input::Question{2024,11,'b'})
    if input.s == ""
        s = strip(test_string_2024_11, '\n')
    else
        s = strip(input.s, '\n')
    end

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

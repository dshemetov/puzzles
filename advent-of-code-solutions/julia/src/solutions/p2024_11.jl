function transform(s::AbstractString)
    if s == "0"
        return ["1"]
    elseif length(s) % 2 == 0
        left_half = parse(Int, s[1:div(end, 2)])
        right_half = parse(Int, s[div(end, 2)+1:end])
        return ["$left_half", "$right_half"]
    else
        return ["$(parse(Int, s) * 2024)"]
    end
end

function solve(input::Question{2024,11,'a'})
    if input.s == ""
        s = test_string_2024_11
    else
        s = input.s
    end
    s = strip(s, '\n')

    d = Dict(x => 1 for x in split(s))
    for _ in 1:25
        d_ = Dict{String,Int}()
        for (k, v) in d
            for k_ in transform(k)
                d_[k_] = get(d_, k_, 0) + v
            end
        end
        d = d_
    end

    return sum(values(d))
end

function solve(input::Question{2024,11,'b'})
    if input.s == ""
        s = test_string_2024_11
    else
        s = input.s
    end
    s = strip(s, '\n')

    d = Dict(x => 1 for x in split(s))
    for _ in 1:75
        d_ = Dict{String,Int}()
        for (k, v) in d
            for k_ in transform(k)
                d_[k_] = get(d_, k_, 0) + v
            end
        end
        d = d_
    end

    return sum(values(d))
end

test_string_2024_11 = """
125 17
"""

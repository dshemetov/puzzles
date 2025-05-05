function solve(input::Question{2024,7,'a'})
    if input.s == ""
        s = test_string_2024_07
    else
        s = input.s
    end
    s = strip(s, '\n')
    lines = [parse.(Int, [y.match for y in eachmatch(r"\d+", x)]) for x in split(s, "\n")]

    total = 0
    for line in lines
        if is_valid1(line[1], line[2:end], false)
            total += line[1]
        end
    end

    return total
end

function solve(input::Question{2024,7,'b'})
    if input.s == ""
        s = test_string_2024_07
    else
        s = input.s
    end
    s = strip(s, '\n')
    lines = [parse.(Int, [y.match for y in eachmatch(r"\d+", x)]) for x in split(s, "\n")]

    total = 0
    for line in lines
        if is_valid2(line[1], line[2:end], true)
            total += line[1]
        end
    end

    return total
end

# My original solution using a vector, takes about 300 ms
function is_valid0(target_value::Int, numbers::Vector{Int}, with_combination::Bool)::Bool
    stack::Vector{Tuple{Int,Vector{Int}}} = [(target_value, numbers)]
    while !isempty(stack)
        current_total, current_numbers = pop!(stack)
        if length(current_numbers) == 1
            if current_total == current_numbers[1]
                return true
            end
            continue
        end

        a, b, rest... = current_numbers
        if current_total < a
            continue
        end

        push!(stack, (current_total, vcat(a + b, rest)))
        push!(stack, (current_total, vcat(a * b, rest)))

        if with_combination
            push!(stack, (current_total, vcat(a * 10^length("$(b)") + b, rest)))
        end
    end
    return false
end

# My vectorized solution, using a dynamically resized vector, takes about 200 ms
function is_valid1(target_value::Int, numbers::Vector{Int}, with_combination::Bool)::Bool
    vals::Vector{Int} = [numbers[1]]
    for num in numbers[2:end]
        if isempty(vals)
            return false
        end
        new_vals = [(vals .+ num)..., (vals .* num)...]
        if with_combination
            append!(new_vals, vals .* 10^length("$(num)") .+ num)
        end
        vals = filter(x -> x <= target_value, new_vals)
    end
    if any(x -> x == target_value, vals)
        return true
    end
    return false
end

# My solution with two buffers pre-allocated (read and write), takes about 160 ms
# (but very dependent on the Array size, which I tweaked with trial and error)
function is_valid2(target_value::Int, numbers::Vector{Int}, with_combination::Bool)::Bool
    vals = Array{Int,2}(undef, 2, 165000)
    vals[1, 1] = numbers[1]
    ri, wi = 1, 2 # read, write
    wj_old = 1
    for num in numbers[2:end]
        wj = 0
        for rj in 1:wj_old
            x = vals[ri, rj]
            xn = x + num
            if xn <= target_value
                wj += 1
                vals[wi, wj] = xn
            end
            xn = x * num
            if xn <= target_value
                wj += 1
                vals[wi, wj] = xn
            end
            if with_combination
                xn = x * 10^length("$(num)") + num
                if xn <= target_value
                    wj += 1
                    vals[wi, wj] = xn
                end
            end
        end
        if wj == 0
            return false
        end
        wj_old = wj
        ri, wi = wi, ri
    end
    for rj in 1:wj_old
        if vals[ri, rj] == target_value
            return true
        end
    end
    return false
end

test_string_2024_07 = """
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
"""

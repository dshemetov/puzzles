# 7. https://adventofcode.com/2024/day/7


function part_a(input::AbstractString)
    s = strip(input, '\n')
    lines::Vector{Vector{Int}} = [parse.(Int, [y.match for y in eachmatch(r"\d+", x)]) for x in split(s, "\n")]

    total::Int = 0
    for line in lines
        if is_valid_reverse(line[1], line[2:end], false)
            total += line[1]
        end
    end

    return total
end

function part_b(input::AbstractString)
    s = strip(input, '\n')
    lines::Vector{Vector{Int}} = [parse.(Int, [y.match for y in eachmatch(r"\d+", x)]) for x in split(s, "\n")]

    total::Int = 0
    for line in lines
        if is_valid_reverse(line[1], line[2:end], true)
            total += line[1]
        end
    end

    return total
end

# My original solution using a vector, takes about 300 ms
function is_valid0(target_value::Int, numbers::Vector{Int}, with_combination::Bool)::Bool
    stack = Tuple{Int,Vector{Int}}[(target_value, numbers)]
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
    vals = Int[numbers[1]]
    sizehint!(vals, 165000)
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

# A kind of ridiculous solution with two buffers pre-allocated (read and write),
# takes about 160 ms (but very dependent on the Array size, which I tweaked with
# trial and error). Very similar to is_valid1, just wanted to see if memory allocation
# was the bottleneck. It's not.
function is_valid2(target_value::Int, numbers::Vector{Int}, with_combination::Bool)::Bool
    vals::Matrix{Int} = Array{Int,2}(undef, 165000, 2)
    vals[1, 1] = numbers[1]
    rj::Int, wj::Int = 1, 2 # read, write
    wi_old::Int = 1
    for num in numbers[2:end]
        wi::Int = 0
        for ri in 1:wi_old
            x::Int = vals[ri, rj]
            xn::Int = x + num
            if xn <= target_value
                wi += 1
                vals[wi, wj] = xn
            end
            xn = x * num
            if xn <= target_value
                wi += 1
                vals[wi, wj] = xn
            end
            if with_combination
                xn = x * 10^length("$(num)") + num
                if xn <= target_value
                    wi += 1
                    vals[wi, wj] = xn
                end
            end
        end
        if wi == 0
            return false
        end
        wi_old = wi
        rj, wj = wj, rj
    end
    for ri in 1:wi_old
        if vals[ri, rj] == target_value
            return true
        end
    end
    return false
end

# Reverse search approach - work backwards from target. Takes about 4ms. This
# approach is key.
function is_valid_reverse(target_value::Int, numbers::Vector{Int}, with_combination::Bool)::Bool
    function backtrack(target::Int, idx::Int)::Bool
        if idx == 1
            return target == numbers[1]
        end

        current_num = numbers[idx]

        # Try subtraction (reverse of addition)
        if target > current_num && backtrack(target - current_num, idx - 1)
            return true
        end

        # Try division (reverse of multiplication)
        if target % current_num == 0 && backtrack(target ÷ current_num, idx - 1)
            return true
        end

        # Try de-concatenation (reverse of concatenation)
        if with_combination
            num_str = string(current_num)
            target_str = string(target)
            if length(target_str) > length(num_str) && endswith(target_str, num_str)
                new_target_str = target_str[1:end-length(num_str)]
                if !isempty(new_target_str)
                    new_target = parse(Int, new_target_str)
                    if backtrack(new_target, idx - 1)
                        return true
                    end
                end
            end
        end

        return false
    end

    return backtrack(target_value, length(numbers))
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

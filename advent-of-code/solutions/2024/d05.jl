# 5. https://adventofcode.com/2024/day/5


function part_a(input::AbstractString)
    s = strip(input, '\n')
    rules_str::String, updates_str::String = split(s, "\n\n")
    rules_nums::Matrix{Int} = parse.(Int, stack([split(x, "|") for x in split(rules_str, "\n")], dims=1))
    m = maximum(rules_nums)
    rules_matrix::BitMatrix = falses(m, m)
    for i in axes(rules_nums, 1)
        rules_matrix[rules_nums[i, 1], rules_nums[i, 2]] = true
    end
    updates::Vector{Vector{Int}} = [parse.(Int, split(x, ",")) for x in split(updates_str, "\n")]

    total::Int = 0
    for update in updates
        valid::Bool = true
        for i in eachindex(update)
            for j in i+1:length(update)
                if !rules_matrix[update[i], update[j]]
                    valid = false
                    break
                end
            end
            if !valid
                break
            end
        end
        if valid
            total += update[cld(length(update), 2)]
        end
    end
    return total
end

function part_b(input::AbstractString)
    s = strip(input, '\n')
    rules_str::String, updates_str::String = split(s, "\n\n")
    rules_nums::Matrix{Int} = parse.(Int, stack([split(x, "|") for x in split(rules_str, "\n")], dims=1))
    m = maximum(rules_nums)
    rules_matrix::BitMatrix = falses(m, m)
    for i in axes(rules_nums, 1)
        rules_matrix[rules_nums[i, 1], rules_nums[i, 2]] = true
    end
    updates::Vector{Vector{Int}} = [parse.(Int, split(x, ",")) for x in split(updates_str, "\n")]

    invalid::Vector{Vector{Int}} = []
    for update in updates
        valid::Bool = true
        for i in eachindex(update)
            for j in i+1:length(update)
                if !rules_matrix[update[i], update[j]]
                    valid = false
                    break
                end
            end
            if !valid
                break
            end
        end
        if !valid
            push!(invalid, update)
        end
    end

    total::Int = 0
    for update in invalid
        for i in eachindex(update)
            for j in i+1:length(update)
                if rules_matrix[update[j], update[i]]
                    update[i], update[j] = update[j], update[i]
                end
            end
        end
        total += update[cld(length(update), 2)]
    end
    return total
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

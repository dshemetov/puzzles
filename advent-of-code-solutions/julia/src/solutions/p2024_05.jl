"""5. https://adventofcode.com/2024/day/5"""


function solve(input::Question{2024,5,'a'})
    if input.s == ""
        s = strip(test_string_2024_05, '\n')
    else
        s = strip(input.s, '\n')
    end
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

function solve(input::Question{2024,5,'b'})
    if input.s == ""
        s = strip(test_string_2024_05, '\n')
    else
        s = strip(input.s, '\n')
    end
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

test_string_2024_05 = """
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
"""

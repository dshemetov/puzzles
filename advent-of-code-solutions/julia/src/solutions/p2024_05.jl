"""5. https://adventofcode.com/2024/day/5"""


function solve(input::Question{2024,5,'a'})
    if input.s == ""
        s = test_string_2024_05
    else
        s = input.s
    end
    s = strip(s, '\n')
    rules_str, updates_str = split(s, "\n\n")
    rules = Set([parse.(Int, split(x, "|")) for x in split(rules_str, "\n")])
    updates = [parse.(Int, split(x, ",")) for x in split(updates_str, "\n")]

    total = 0
    for update in updates
        valid = true
        for i in eachindex(update)
            for j in range(i + 1, length(update))
                if [update[i], update[j]] ∉ rules
                    valid = false
                    break
                end
            end
            if !valid
                break
            end
        end
        if valid
            total += update[Int(ceil(length(update) / 2))]
        end
    end
    return total
end

function solve(input::Question{2024,5,'b'})
    if input.s == ""
        s = test_string_2024_05
    else
        s = input.s
    end
    s = strip(s, '\n')
    rules_str, updates_str = split(s, "\n\n")
    rules = Set([parse.(Int, split(x, "|")) for x in split(rules_str, "\n")])
    updates = [parse.(Int, split(x, ",")) for x in split(updates_str, "\n")]

    invalid = []
    for update in updates
        valid = true
        for i in eachindex(update)
            for j in i+1:length(update)
                if [update[i], update[j]] ∉ rules
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

    total = 0
    for update in invalid
        for i in eachindex(update)
            for j in i+1:length(update)
                if [update[j], update[i]] in rules
                    update[i], update[j] = update[j], update[i]
                end
            end
        end
        total += update[Int(ceil(length(update) / 2))]
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

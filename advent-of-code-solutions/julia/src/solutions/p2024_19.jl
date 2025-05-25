function solve(input::Question{2024,19,'a'})
    if input.s == ""
        s = test_string_2024_19
    else
        s = input.s
    end
    first, last = split(s, "\n\n")
    options = split(strip(first), ", ")
    targets = split(strip(last), "\n")
    option_lengths = length.(options)
    cache = Dict{String, Bool}()

    function recurse(prefix, target)
        if prefix == target
            return true
        end

        prefix_len = length(prefix)
        target_len = length(target)

        for (i, option) in enumerate(options)
            if prefix_len + option_lengths[i] > target_len
                continue
            end
            if prefix * option == target[1:prefix_len + option_lengths[i]]
                res = get!(cache, prefix * option) do
                    recurse(prefix * option, target)
                end
                if res
                    return true
                end
                cache[prefix] = res
            end
        end
        return false
    end

    total = 0
    for target in targets
        cache = Dict{String, Bool}()
        if recurse("", target)
            total += 1
        end
    end

    return total
end


function solve(input::Question{2024,19,'b'})
    if input.s == ""
        s = test_string_2024_19
    else
        s = input.s
    end
    first, last = split(s, "\n\n")
    options = split(strip(first), ", ")
    targets = split(strip(last), "\n")
    option_lengths = length.(options)
    cache = Dict{String, Int}()

    function recurse(prefix, target)
        if prefix == target
            return true
        end

        prefix_len = length(prefix)
        target_len = length(target)

        target_total = 0
        for (i, option) in enumerate(options)
            if prefix_len + option_lengths[i] > target_len
                continue
            end
            if prefix * option == target[1:prefix_len + option_lengths[i]]
                res = get!(cache, prefix * option) do
                    recurse(prefix * option, target)
                end
                target_total += res
            end
        end
        cache[prefix] = target_total
        return target_total
    end

    total = 0
    for target in targets
        cache = Dict{String, Int}()
        total += recurse("", target)
    end

    return total
end

test_string_2024_19 = """
r, wr, b, g, bwu, rb, gb, br

brwrr
bggr
gbbr
rrbgbr
ubwu
bwurrg
brgr
bbrgwb
"""
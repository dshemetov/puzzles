"""19. https://adventofcode.com/2024/day/19

The dynamic programming part is really interesting.
It's much faster than the recursive + memoized approach, about 5x faster.

The dynamic programming recursive relation is:
    dp[i] = sum(dp[j] for j in max(1, i - max_len):(i-1) if target[j:(i-1)] in options)
    dp[1] = 1

In words, dp[i] is the number of ways to form the first i characters of the target string using the given options.

The base case is dp[1] = 1, because there is one way to form the empty string.

In the recursive case, for a given state i, we try all shorter prefixes of the target string and see if there exists a prefix of the right length to get to i.
If so, we add the number of ways to get to the shorter prefix to the number of ways to get to i.

The max_len is the maximum length of the options, which helps reduce the number of previous states we need to consider.
"""

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
    max_len = maximum(option_lengths)

    total = 0
    for target in targets
        dp = zeros(Int, length(target) + 1)
        dp[1] = 1
        for i in 2:length(dp)
            for j in max(1, i - max_len):(i-1)
                if target[j:(i-1)] in options
                    dp[i] += dp[j]
                end
            end
        end
        total += dp[end]
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
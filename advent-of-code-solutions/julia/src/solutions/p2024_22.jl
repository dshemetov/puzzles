"""22. https://adventofcode.com/2024/day/22"""

function solve(input::Question{2024,22,'a'})
    if input.s == ""
        s = strip(test_string_2024_22_a, '\n')
    else
        s = strip(input.s, '\n')
    end
    n = 2000
    s = split(s, "\n")
    total = 0
    for line in s
        sn = parse(Int, line)
        for _ in 1:n
            sn = next_num(sn)
        end
        total += sn
    end
    return total
end

function next_num(n::Int)::Int
    prune_mask = (1 << 24) - 1
    n = ((n << 6) ⊻ n) & prune_mask
    n = ((n >> 5) ⊻ n) & prune_mask
    n = ((n << 11) ⊻ n) & prune_mask
    return n
end

function solve(input::Question{2024,22,'b'})
    if input.s == ""
        s = strip(test_string_2024_22_b, '\n')
    else
        s = strip(input.s, '\n')
    end
    s = split(s, "\n")
    n, m = 2000, length(s)

    # Get prices for each monkey.
    ps = zeros(Int8, (n + 1, m)) # (n + 1, m)
    for (i, line) in enumerate(s)
        sn = parse(Int, line)
        ps[1, i] = sn % 10
        for j in 1:n
            sn = next_num(sn)
            ps[j+1, i] = sn % 10
        end
    end

    # Get price changes for each monkey. Range is [-9, 9], so shift up by 9 to
    # avoid negative indices.
    pds = diff(ps, dims=1) .+ 9 # (n, m)

    # Scan through each monkey's price changes, creating 4-digit prefixes, and
    # tallying the profits for each prefix. Dictionaries are slow, so we use a
    # custom base 19 index into a 1D array.
    prefix_profits = zeros(Int32, 19^4)
    for i in 1:m
        seen = falses(19^4)
        for j in 1:n-3
            index = pds[j, i] * 19^3 + pds[j+1, i] * 19^2 + pds[j+2, i] * 19 + pds[j+3, i]
            # Only the first occurrence matters.
            if !seen[index]
                # pds[j+3, i] = ps[j+4, i] - ps[j+3, i]
                # so ps[j+4, i] is the current price.
                prefix_profits[index] += ps[j+4, i]
                seen[index] = true
            end
        end
    end

    return maximum(prefix_profits)
end

test_string_2024_22_a = """
1
10
100
2024
"""

test_string_2024_22_b = """
1
2
3
2024
"""
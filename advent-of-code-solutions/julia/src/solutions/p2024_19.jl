function solve(input::Question{2024,19,'a'})
    if input.s == ""
        s = test_string_2024_19
    else
        s = input.s
    end
    first, last = split(s, "\n\n")
    options = split(strip(first), ", ")
    targets = split(strip(last), "\n")

    cache = Dict{String, Bool}()

    function recurse(prefix, target)
        if length(prefix) > length(target)
            return false
        end

        if prefix == target
            return true
        end

        out = []
        for option in options
            if length(prefix * option) > length(target)
                continue
            end
            if prefix * option == target[1:length(prefix * option)]
                if haskey(cache, prefix * option)
                    out = vcat(out, cache[prefix * option])
                else
                    res = recurse(prefix * option, target)
                    out = vcat(out, res)
                    cache[prefix * option] = res
                end
            end
        end
        return any(out)
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

    cache = Dict{String, Int}()

    function recurse(prefix, target)
        if length(prefix) > length(target)
            return false
        end

        if prefix == target
            return true
        end

        out = []
        for option in options
            if length(prefix * option) > length(target)
                continue
            end
            if prefix * option == target[1:length(prefix * option)]
                if haskey(cache, prefix * option)
                    out = vcat(out, cache[prefix * option])
                else
                    res = recurse(prefix * option, target)
                    out = vcat(out, res)
                    cache[prefix * option] = res
                end
            end
        end
        if length(out) == 0
            return 0
        else
            return sum(out)
        end
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
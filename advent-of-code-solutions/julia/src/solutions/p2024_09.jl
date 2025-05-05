import Base: length, <, -

struct Range
    start::Int
    stop::Int
end

function length(r::Range)
    return r.stop - r.start + 1
end

function -(r1::Range, r2::Range)
    # new memory, old memory, new file
    if length(r1) > length(r2)
        return Range(r1.start + length(r2), r1.stop), Range(r1.start, r1.start + length(r2) - 1), nothing
    elseif length(r1) == length(r2)
        return nothing, r1, nothing
    else
        return nothing, r1, Range(r2.start, r2.stop - length(r1))
    end
end

function <(r1::Range, r2::Range)
    return r1.stop < r2.start
end

function view_memory(mem, nums)
    # Let's print the final state of the memory
    arr = zeros(Int, sum(nums))
    arr .= -1
    for (k, v) in mem
        if k == -1
            continue
        end
        for r in v
            arr[1+r.start:(r.stop+1)] .= k
        end
    end
    arr = join([c != -1 ? string(c) : "." for c in arr])
    println(arr)
end

function solve(input::Question{2024,9,'a'})
    if input.s == ""
        s = test_string_2024_9
    else
        s = input.s
    end
    s = strip(s, '\n')
    nums = [parse(Int, c) for c in s]

    m = Dict{Int,Vector{Range}}()
    i = 0
    for (j, n) in enumerate(nums)
        if n == 0
            continue
        end
        if j % 2 == 1
            push!(get!(m, (j - 1) / 2, []), Range(i, i + n - 1))
        else
            # -1 is the index of free memory
            push!(get!(m, -1, []), Range(i, i + n - 1))
        end
        i += n
    end
    push!(get!(m, -1, []), Range(i + 1, i + 1))

    j = maximum([k for (k, v) in m if k != -1])
    while m[-1][1] < m[j][end]
        x, y = m[-1][1], m[j][end]
        z = x - y

        # case 1: file fits into memory block with space left
        # case 2: file fits exactly into memory block
        # case 3: file is larger than memory block
        if !isnothing(z[1])
            insert!(m[j], length(m[j]), z[2])
            m[j] = m[j][1:end-1]
            m[-1][1] = z[1]
            j -= 1
        elseif isnothing(z[1]) && isnothing(z[3])
            insert!(m[j], length(m[j]), z[2])
            m[j] = m[j][1:end-1]
            m[-1] = m[-1][2:end]
            j -= 1
        else
            insert!(m[j], length(m[j]), z[2])
            m[j][end] = z[3]
            m[-1] = m[-1][2:end]
        end
    end

    return sum(k * sum(r.start:r.stop) for (k, v) in m for r in v if k != -1)
end

function solve(input::Question{2024,9,'b'})
    if input.s == ""
        s = test_string_2024_9
    else
        s = input.s
    end
    s = strip(s, '\n')
    nums = [parse(Int, c) for c in s]

    m = Dict{Int,Vector{Range}}()
    i = 0
    for (j, n) in enumerate(nums)
        if n == 0
            continue
        end
        if j % 2 == 1
            push!(get!(m, (j - 1) / 2, []), Range(i, i + n - 1))
        else
            # -1 is the index of free memory
            push!(get!(m, -1, []), Range(i, i + n - 1))
        end
        i += n
    end
    push!(get!(m, -1, []), Range(i + 1, i + 1))

    # view_memory(m, nums)
    j = maximum([k for (k, v) in m if k != -1])
    while m[-1][1] < m[j][end] && j >= 0
        file_size = length(m[j][end])

        # find a free block that can fully fit the file block
        i = nothing
        for (k, r) in enumerate(m[-1])
            # stop looking if the memory blocks are to the right of the file block
            if m[j][end] < r
                break
            end
            if length(r) >= file_size
                i = k
                break
            end
        end

        if isnothing(i)
            j -= 1
            continue
        end

        z = m[-1][i] - m[j][end]
        # case 1: file fits into memory block with space left
        # case 2: file fits exactly into memory block
        insert!(m[j], length(m[j]), z[2])
        m[j] = m[j][1:end-1]
        if !isnothing(z[1])
            m[-1][i] = z[1]
        else
            deleteat!(m[-1], i)
        end
        j -= 1
        # view_memory(m, nums)
    end

    return sum(k * sum(r.start:r.stop) for (k, v) in m for r in v if k != -1)
end

test_string_2024_9 = """
2333133121414131402
"""

test_string_2024_9b = """
9239692674378649238
"""

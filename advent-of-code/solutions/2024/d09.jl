# 9. https://adventofcode.com/2024/day/9
# Alternative approach: d09-blocks.jl

# Direct array representation. With SIMD and cache-friendly access, this is the
# fastest solution.
function part_a(input::AbstractString)
    s = strip(input, '\n')

    # Parse input and calculate total size
    nums::Vector{Int8} = [parse(Int8, c) for c in s]
    total_size::Int = sum(nums)

    # Create disk representation directly
    disk::Vector{Int16} = Vector{Int16}(undef, total_size)
    pos::Int = 1

    for (i, n) in enumerate(nums)
        if n == 0
            continue
        end

        if i % 2 == 1  # File
            file_id::Int16 = Int16(i ÷ 2)
            for j in 1:n
                disk[pos] = file_id
                pos += 1
            end
        else  # Free space
            for j in 1:n
                disk[pos] = Int16(-1)
                pos += 1
            end
        end
    end

    # Two-pointer defragmentation
    left::Int = 1
    right::Int = total_size

    while left < right
        # Find next free space from left
        while left <= total_size && disk[left] != -1
            left += 1
        end

        # Find next file block from right
        while right >= 1 && disk[right] == -1
            right -= 1
        end

        if left >= right
            break
        end

        # Move block
        disk[left] = disk[right]
        disk[right] = -1
        left += 1
        right -= 1
    end

    # Calculate checksum
    checksum::Int = 0
    for (pos, file_id) in enumerate(disk)
        if file_id != -1
            checksum += Int(file_id) * (pos - 1)
        end
    end

    return checksum
end

function part_b(input::AbstractString)
    s = strip(input, '\n')

    # Parse and create file/free space lists
    nums = Int8[parse(Int8, c) for c in s]

    # Pre-allocate arrays for file and free space tracking
    max_files = (length(nums) + 1) ÷ 2
    file_positions = Vector{Int}(undef, max_files)
    file_sizes = Vector{Int8}(undef, max_files)

    free_positions = Int[]
    free_sizes = Int8[]

    pos = 0
    file_count = 0

    for (i, n) in enumerate(nums)
        if n == 0
            pos += n
            continue
        end

        if i % 2 == 1  # File
            file_count += 1
            file_positions[file_count] = pos
            file_sizes[file_count] = n
        else  # Free space
            push!(free_positions, pos)
            push!(free_sizes, n)
        end
        pos += n
    end

    # Resize arrays to actual size
    resize!(file_positions, file_count)
    resize!(file_sizes, file_count)

    # Process files from highest ID to lowest
    for file_id in file_count:-1:1
        file_pos = file_positions[file_id]
        file_size = file_sizes[file_id]

        # Find leftmost free space that can fit this file
        for (i, free_pos) in enumerate(free_positions)
            if free_pos >= file_pos  # Don't move right
                break
            end

            if free_sizes[i] >= file_size
                # Move the file
                file_positions[file_id] = free_pos

                # Update free space
                if free_sizes[i] == file_size
                    # Exact fit - remove free space
                    deleteat!(free_positions, i)
                    deleteat!(free_sizes, i)
                else
                    # Partial fit - update free space
                    free_positions[i] += file_size
                    free_sizes[i] -= file_size
                end
                break
            end
        end
    end

    # Calculate checksum
    checksum::Int = 0
    for file_id in 1:file_count
        pos = file_positions[file_id]
        size = Int(file_sizes[file_id])
        for offset in 0:(size-1)
            checksum += (file_id - 1) * (pos + offset)
        end
    end

    return checksum
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

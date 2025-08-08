"""9. https://adventofcode.com/2024/day/9"""

struct Block
    id::Int      # file ID (-1 for free space)
    start::Int   # start position
    size::Int    # block size
end

# Block-based solution
function solve_block(input::Question{2024,9,'a'})
    if input.s == ""
        s = strip(test_string_2024_9, '\n')
    else
        s = strip(input.s, '\n')
    end
    nums = Int[parse(Int, c) for c in s]

    # Create a more efficient representation using a simple vector of blocks
    blocks = Block[]
    pos = 0

    for (i, n) in enumerate(nums)
        if n == 0
            continue
        end
        if i % 2 == 1  # File
            file_id::Int = (i - 1) ÷ 2
            push!(blocks, Block(file_id, pos, n))
        else  # Free space
            push!(blocks, Block(-1, pos, n))
        end
        pos += n
    end

    # Defragmentation using two pointers
    left::Int = 1
    right::Int = length(blocks)

    while left < right
        # Find next free space from left
        while left <= length(blocks) && blocks[left].id != -1
            left += 1
        end

        # Find next file from right
        while right >= 1 && blocks[right].id == -1
            right -= 1
        end

        if left >= right
            break
        end

        free_block = blocks[left]
        file_block = blocks[right]

        if free_block.size >= file_block.size
            # File fits completely
            blocks[left] = Block(file_block.id, free_block.start, file_block.size)
            blocks[right] = Block(-1, file_block.start, file_block.size)

            if free_block.size > file_block.size
                # Insert remaining free space
                remaining = Block(-1, free_block.start + file_block.size,
                    free_block.size - file_block.size)
                insert!(blocks, left + 1, remaining)
                right += 1  # Adjust for insertion
            end
            right -= 1
        else
            # File is larger than free space - partial move
            blocks[left] = Block(file_block.id, free_block.start, free_block.size)
            blocks[right] = Block(file_block.id, file_block.start,
                file_block.size - free_block.size)
            left += 1
        end
    end

    # Calculate checksum
    checksum::Int = 0
    for block in blocks
        if block.id != -1
            for pos in block.start:(block.start+block.size-1)
                checksum += block.id * pos
            end
        end
    end

    return checksum
end

function solve_block(input::Question{2024,9,'b'})
    if input.s == ""
        s = strip(test_string_2024_9, '\n')
    else
        s = strip(input.s, '\n')
    end
    nums = Int[parse(Int, c) for c in s]

    # Create blocks representation
    blocks = Block[]
    pos = 0

    for (i, n) in enumerate(nums)
        if n == 0
            continue
        end
        if i % 2 == 1  # File
            file_id::Int = (i - 1) ÷ 2
            push!(blocks, Block(file_id, pos, n))
        else  # Free space
            push!(blocks, Block(-1, pos, n))
        end
        pos += n
    end

    # Get max file ID and work backwards
    max_file_id = maximum(block.id for block in blocks if block.id != -1)

    for file_id in max_file_id:-1:0
        # Find the file block
        file_idx::Int = 0
        for (i, block) in enumerate(blocks)
            if block.id == file_id
                file_idx = i
                break
            end
        end

        if file_idx == 0
            continue
        end

        file_block = blocks[file_idx]

        # Find leftmost free space that can fit this file
        for (i, block) in enumerate(blocks)
            if i >= file_idx  # Don't move right
                break
            end

            if block.id == -1 && block.size >= file_block.size
                # Move the file
                blocks[i] = Block(file_block.id, block.start, file_block.size)
                blocks[file_idx] = Block(-1, file_block.start, file_block.size)

                # Handle remaining free space
                if block.size > file_block.size
                    remaining = Block(-1, block.start + file_block.size,
                        block.size - file_block.size)
                    insert!(blocks, i + 1, remaining)
                end
                break
            end
        end
    end

    # Calculate checksum
    checksum::Int = 0
    for block in blocks
        if block.id != -1
            for pos in block.start:(block.start+block.size-1)
                checksum += block.id * pos
            end
        end
    end

    return checksum
end

# Direct array representation. With SIMD and cache-friendly access, this is the
# fastest solution.
function solve_fastest(input::Question{2024,9,'a'})
    if input.s == ""
        s = strip(test_string_2024_9, '\n')
    else
        s = strip(input.s, '\n')
    end

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

function solve_fastest(input::Question{2024,9,'b'})
    if input.s == ""
        s = strip(test_string_2024_9, '\n')
    else
        s = strip(input.s, '\n')
    end

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

function solve(input::Question{2024,9,'a'}, method::String="fastest")
    if method == "block"
        return solve_block(input)
    elseif method == "fastest"
        return solve_fastest(input)
    else
        error("Unknown method: $method. Available methods: 'block', 'fastest'")
    end
end

function solve(input::Question{2024,9,'b'}, method::String="fastest")
    if method == "block"
        return solve_block(input)
    elseif method == "fastest"
        return solve_fastest(input)
    else
        error("Unknown method: $method. Available methods: 'block', 'fastest'")
    end
end

test_string_2024_9 = """
2333133121414131402
"""

test_string_2024_9b = """
9239692674378649238
"""

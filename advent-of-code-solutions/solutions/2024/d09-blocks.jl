# 9. https://adventofcode.com/2024/day/9
# Variant of d09.jl: tracks files and free space as blocks (same answers, slower).

struct Block
    id::Int      # file ID (-1 for free space)
    start::Int   # start position
    size::Int    # block size
end

# Block-based solution
function part_a(input::AbstractString)
    s = strip(input, '\n')
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

function part_b(input::AbstractString)
    s = strip(input, '\n')
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
test_string_2024_9 = """
2333133121414131402
"""

test_string_2024_9b = """
9239692674378649238
"""

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

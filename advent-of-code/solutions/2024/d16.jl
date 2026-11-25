# 16. https://adventofcode.com/2024/day/16
# Alternative approach: d16-dict.jl

using DataStructures: PriorityQueue, enqueue!, dequeue!

const DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

function part_a(input::AbstractString)
    s = strip(input, '\n')

    lines = split(s, '\n')
    m, n = length(lines), length(lines[1])

    # More efficient grid representation
    grid = Matrix{UInt8}(undef, m, n)
    start_pos = (0, 0)
    end_pos = (0, 0)

    for (i, line) in enumerate(lines)
        for (j, char) in enumerate(line)
            grid[i, j] = UInt8(char)
            if char == 'S'
                start_pos = (i, j)
            elseif char == 'E'
                end_pos = (i, j)
            end
        end
    end

    # Use 3D array instead of dictionary for costs (i, j, direction)
    costs = fill(typemax(Int32), m, n, 4)
    costs[start_pos[1], start_pos[2], 1] = 0  # Start facing east (direction 1)

    # Priority queue with better state representation
    queue = PriorityQueue{Tuple{Int,Int,Int},Int}()
    enqueue!(queue, (start_pos[1], start_pos[2], 1) => 0)

    while !isempty(queue)
        (i, j, dir) = dequeue!(queue)
        current_cost = costs[i, j, dir]

        if (i, j) == end_pos
            return current_cost
        end

        # Try all 4 directions
        for new_dir in 1:4
            di, dj = DIRS[new_dir]
            ni, nj = i + di, j + dj

            # Check bounds and walls
            if ni < 1 || ni > m || nj < 1 || nj > n || grid[ni, nj] == UInt8('#')
                continue
            end

            # Calculate cost (1000 for turns, 1 for movement)
            turn_cost = (dir != new_dir) ? 1000 : 0
            new_cost = current_cost + 1 + turn_cost

            if new_cost < costs[ni, nj, new_dir]
                costs[ni, nj, new_dir] = new_cost
                # Add Manhattan distance heuristic
                h = abs(ni - end_pos[1]) + abs(nj - end_pos[2])
                state = (ni, nj, new_dir)
                # Remove existing state if present (PriorityQueue requires unique keys)
                if haskey(queue, state)
                    delete!(queue, state)
                end
                enqueue!(queue, state => new_cost + h)
            end
        end
    end

    return -1  # No path found
end

function part_b(input::AbstractString)
    s = strip(input, '\n')

    lines = split(s, '\n')
    m, n = length(lines), length(lines[1])

    # More efficient grid representation
    grid = Matrix{UInt8}(undef, m, n)
    start_pos = (0, 0)
    end_pos = (0, 0)

    for (i, line) in enumerate(lines)
        for (j, char) in enumerate(line)
            grid[i, j] = UInt8(char)
            if char == 'S'
                start_pos = (i, j)
            elseif char == 'E'
                end_pos = (i, j)
            end
        end
    end

    # Use 3D array for costs and track predecessors efficiently
    costs = fill(typemax(Int32), m, n, 4)
    costs[start_pos[1], start_pos[2], 1] = 0

    # Track predecessors for each state
    predecessors = Dict{Tuple{Int,Int,Int},Vector{Tuple{Int,Int,Int}}}()
    predecessors[(start_pos[1], start_pos[2], 1)] = []

    # Priority queue for Dijkstra's algorithm
    queue = PriorityQueue{Tuple{Int,Int,Int},Int}()
    enqueue!(queue, (start_pos[1], start_pos[2], 1) => 0)

    while !isempty(queue)
        (i, j, dir) = dequeue!(queue)
        current_cost = costs[i, j, dir]

        # Try all 4 directions
        for new_dir in 1:4
            di, dj = DIRS[new_dir]
            ni, nj = i + di, j + dj

            # Check bounds and walls
            if ni < 1 || ni > m || nj < 1 || nj > n || grid[ni, nj] == UInt8('#')
                continue
            end

            # Calculate cost
            turn_cost = (dir != new_dir) ? 1000 : 0
            new_cost = current_cost + 1 + turn_cost
            new_state = (ni, nj, new_dir)

            if new_cost < costs[ni, nj, new_dir]
                # Found better path
                costs[ni, nj, new_dir] = new_cost
                predecessors[new_state] = [(i, j, dir)]

                # Remove existing state if present
                if haskey(queue, new_state)
                    delete!(queue, new_state)
                end
                h = abs(ni - end_pos[1]) + abs(nj - end_pos[2])
                enqueue!(queue, new_state => new_cost + h)

            elseif new_cost == costs[ni, nj, new_dir]
                # Found equally good path
                if haskey(predecessors, new_state)
                    push!(predecessors[new_state], (i, j, dir))
                else
                    predecessors[new_state] = [(i, j, dir)]
                end
            end
        end
    end

    # Find minimum cost to reach end
    min_end_cost = typemax(Int32)
    for dir in 1:4
        min_end_cost = min(min_end_cost, costs[end_pos[1], end_pos[2], dir])
    end

    # Backtrack from all optimal end states
    on_optimal_path = falses(m, n)
    visited_states = Set{Tuple{Int,Int,Int}}()
    queue_back = Vector{Tuple{Int,Int,Int}}()

    # Start from all end positions with minimum cost
    for dir in 1:4
        if costs[end_pos[1], end_pos[2], dir] == min_end_cost
            state = (end_pos[1], end_pos[2], dir)
            push!(queue_back, state)
            push!(visited_states, state)
        end
    end

    while !isempty(queue_back)
        state = pop!(queue_back)
        i, j, dir = state
        on_optimal_path[i, j] = true

        if haskey(predecessors, state)
            for pred_state in predecessors[state]
                if pred_state ∉ visited_states
                    push!(visited_states, pred_state)
                    push!(queue_back, pred_state)
                end
            end
        end
    end

    return count(on_optimal_path)
end

test_string_2024_16 = """
###############
#.......#....E#
#.#.###.#.###.#
#.....#.#...#.#
#.###.#####.#.#
#.#.#.......#.#
#.#.#####.###.#
#...........#.#
###.#.#####.#.#
#...#.....#.#.#
#.#.#.###.#.#.#
#.....#...#.#.#
#.###.#.#.#.#.#
#S..#.....#...#
###############
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

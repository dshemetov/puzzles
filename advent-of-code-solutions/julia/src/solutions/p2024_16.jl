"""16. https://adventofcode.com/2024/day/16"""

using DataStructures: PriorityQueue, enqueue!, dequeue!

const DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

function solve_optimized(input::Question{2024,16,'a'})
    if input.s == ""
        s = strip(test_string_2024_16, '\n')
    else
        s = strip(input.s, '\n')
    end

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

function solve_optimized(input::Question{2024,16,'b'})
    if input.s == ""
        s = strip(test_string_2024_16, '\n')
    else
        s = strip(input.s, '\n')
    end

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

function solve(input::Question{2024,16,'a'}, method::String="optimized")
    if method == "original"
        return solve_original(input)
    elseif method == "optimized"
        return solve_optimized(input)
    else
        error("Unknown method: $method. Available methods: 'original', 'optimized'")
    end
end

function solve(input::Question{2024,16,'b'}, method::String="optimized")
    if method == "original"
        return solve_original(input)
    elseif method == "optimized"
        return solve_optimized(input)
    else
        error("Unknown method: $method. Available methods: 'original', 'optimized'")
    end
end

function solve_original(input::Question{2024,16,'a'})
    if input.s == ""
        s = strip(test_string_2024_16, '\n')
    else
        s = strip(input.s, '\n')
    end
    grid = stack([collect(row) for row in split(s, '\n')], dims=1)
    m, n = size(grid)

    start_pos = Tuple(findfirst(==('S'), grid))
    end_pos = Tuple(findfirst(==('E'), grid))

    # A* search
    function h((pos, _))  # heuristic function - manhattan distance
        return abs(pos[1] - end_pos[1]) + abs(pos[2] - end_pos[2])
    end

    queue = PriorityQueue()
    came_from = Dict{Any,Any}() # Track path

    # Start facing east
    enqueue!(queue, (start_pos, 1) => 0)
    came_from[(start_pos, 1)] = nothing

    costs = Dict{Tuple{Tuple{Int,Int},Int},Int}()
    costs[(start_pos, 1)] = 0
    final_state = nothing
    while !isempty(queue)
        current_state = dequeue!(queue)
        (pos, dir) = current_state
        cost = costs[(pos, dir)]
        if pos == end_pos
            final_state = current_state
            break
        end

        # Try all directions
        for (new_dir, dv) in enumerate(DIRS)
            new_pos = pos .+ dv

            # Check bounds and walls
            if new_pos[1] < 1 || new_pos[1] > m || new_pos[2] < 1 || new_pos[2] > n
                continue
            end
            if grid[new_pos...] == '#'
                continue
            end

            # Calculate new cost (1000 for turns, 1 for movement)
            turn_cost = (dir != new_dir) ? 1000 : 0
            new_cost = cost + 1 + turn_cost
            new_state = (new_pos, new_dir)

            if !haskey(costs, new_state) || new_cost < costs[new_state]
                costs[new_state] = new_cost
                # Evacuate old state (otherwise we might get duplicates and
                # that's not allowed)
                if haskey(queue, new_state)
                    delete!(queue, new_state)
                end
                enqueue!(queue, new_state => new_cost + h(new_state))
                came_from[new_state] = current_state
            end
        end
    end

    if final_state === nothing
        return -1  # No path found
    end

    # Reconstruct and visualize path
    # path = []
    # current = final_state
    # while current !== nothing
    #     pushfirst!(path, current)
    #     current = came_from[current]
    # end

    # # Create visualization grid
    # viz_grid = copy(grid)
    # dir_chars = ['>', 'v', '<', '^']

    # for ((y, x), dir) in path
    #     if viz_grid[y, x] ∉ ['S', 'E']
    #         viz_grid[y, x] = dir_chars[dir]
    #     end
    # end

    # println("Path visualization:")
    # print_grid(viz_grid)

    return costs[final_state]
end

function solve_original(input::Question{2024,16,'b'})
    if input.s == ""
        s = strip(test_string_2024_16, '\n')
    else
        s = strip(input.s, '\n')
    end
    grid = stack([collect(row) for row in split(s, '\n')], dims=1)
    m, n = size(grid)

    start_pos = Tuple(findfirst(==('S'), grid))
    end_pos = Tuple(findfirst(==('E'), grid))

    # A* search
    function h((pos, _))  # heuristic function - manhattan distance
        return abs(pos[1] - end_pos[1]) + abs(pos[2] - end_pos[2])
    end

    queue = PriorityQueue()
    came_from = Dict{Any,Set{Any}}() # Track all optimal predecessors
    came_from[(start_pos, 1)] = Set([nothing])

    # Start facing east
    enqueue!(queue, (start_pos, 1) => 0)

    costs = Dict{Tuple{Tuple{Int,Int},Int},Int}()
    costs[(start_pos, 1)] = 0
    final_state = nothing
    while !isempty(queue)
        current_state = dequeue!(queue)
        (pos, dir) = current_state
        cost = costs[(pos, dir)]
        if pos == end_pos
            final_state = current_state
            break
        end

        # Try all directions
        for (new_dir, dv) in enumerate(DIRS)
            new_pos = pos .+ dv

            # Check bounds and walls
            if new_pos[1] < 1 || new_pos[1] > m || new_pos[2] < 1 || new_pos[2] > n
                continue
            end
            if grid[new_pos...] == '#'
                continue
            end

            # Calculate new cost (1000 for turns, 1 for movement)
            turn_cost = (dir != new_dir) ? 1000 : 0
            new_cost = cost + 1 + turn_cost
            new_state = (new_pos, new_dir)
            if !haskey(costs, new_state)
                costs[new_state] = new_cost
                came_from[new_state] = Set([current_state])
                # Evacuate old state
                if haskey(queue, new_state)
                    delete!(queue, new_state)
                end
                enqueue!(queue, new_state => new_cost + h(new_state))
            elseif new_cost == costs[new_state]
                push!(came_from[new_state], current_state)
                # Evacuate old state
                if haskey(queue, new_state)
                    delete!(queue, new_state)
                end
                enqueue!(queue, new_state => new_cost + h(new_state))
            end
        end
    end

    if final_state === nothing
        return -1  # No path found
    end

    # Make a set of all the predecessors that belong to a shortest path
    node_set = Set{Tuple{Int,Int}}()
    queue = Set([final_state])
    while !isempty(queue)
        current = pop!(queue)
        push!(node_set, current[1])
        for pred in came_from[current]
            if pred === nothing
                continue
            end
            push!(queue, pred)
        end
    end

    # Reconstruct and visualize path
    # path = []
    # current = final_state
    # while current !== nothing
    #     pushfirst!(path, current)
    #     current = came_from[current]
    # end

    # # Create visualization grid
    # viz_grid = copy(grid)
    # dir_chars = ['>', 'v', '<', '^']

    # for ((y, x), dir) in path
    #     if viz_grid[y, x] ∉ ['S', 'E']
    #         viz_grid[y, x] = dir_chars[dir]
    #     end
    # end

    # println("Path visualization:")
    # print_grid(viz_grid)

    return length(node_set)
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


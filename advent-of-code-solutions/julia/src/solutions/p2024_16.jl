using DataStructures: PriorityQueue, enqueue!, dequeue!

const DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]

function solve(input::Question{2024,16,'a'})
    if input.s == ""
        s = test_string_2024_16
    else
        s = input.s
    end
    s = strip(s, '\n')
    grid = stack([collect(row) for row in split(s, '\n')], dims=1)
    m, n = size(grid)

    start_pos = Tuple(findfirst(==('S'), grid))
    end_pos = Tuple(findfirst(==('E'), grid))
    # println(start_pos)
    # println(end_pos)

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

function solve(input::Question{2024,16,'b'})
    if input.s == ""
        s = test_string_2024_16
    else
        s = input.s
    end
    s = strip(s, '\n')
    grid = stack([collect(row) for row in split(s, '\n')], dims=1)
    m, n = size(grid)

    start_pos = Tuple(findfirst(==('S'), grid))
    end_pos = Tuple(findfirst(==('E'), grid))
    # println(start_pos)
    # println(end_pos)

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

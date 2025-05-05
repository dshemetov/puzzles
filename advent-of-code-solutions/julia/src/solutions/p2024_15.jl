function solve(input::Question{2024,15,'a'})
    s = isempty(input.s) ? test_string_2024_15_a : input.s
    s = strip(s, '\n')
    grid, path = split(s, "\n\n")
    grid = string_to_char_matrix(grid)
    path = replace(path, '\n' => "")
    m, n = size(grid)

    cur = Tuple(findfirst(==('@'), grid))
    dirs = Dict('>' => (0, 1), '<' => (0, -1), '^' => (-1, 0), 'v' => (1, 0))
    for i in eachindex(path)
        dir = dirs[path[i]]
        cur_ = cur
        while true
            cur_ = cur_ .+ dir
            if grid[cur_[1], cur_[2]] == '#'
                break
            end
            if grid[cur_[1], cur_[2]] == '.'
                break
            end
        end
        if grid[cur_[1], cur_[2]] == '#'
            continue
        end
        xmin, xmax = min(cur[1], cur_[1]), max(cur[1], cur_[1])
        ymin, ymax = min(cur[2], cur_[2]), max(cur[2], cur_[2])
        grid[xmin:xmax, ymin:ymax] = circshift(grid[xmin:xmax, ymin:ymax], dir)
        cur = cur .+ dir
    end
    return score(grid)
end

function score(grid)
    m, n = size(grid)
    return sum((i - 1) * 100 + (j - 1) for i in 1:m, j in 1:n if grid[i, j] in ['O', '['])
end

function solve(input::Question{2024,15,'b'})
    s = isempty(input.s) ? test_string_2024_15_b : input.s
    s = strip(s, '\n')
    s = replace(s, "#" => "##", "@" => "@.", "O" => "[]", "." => "..")
    grid, path = split(s, "\n\n")
    grid = string_to_char_matrix(grid)
    path = replace(path, '\n' => "")
    m, n = size(grid)

    cur = Tuple(findfirst(==('@'), grid))
    dirs = Dict('>' => (0, 1), '<' => (0, -1), '^' => (-1, 0), 'v' => (1, 0))
    for i in eachindex(path)
        dir = dirs[path[i]]
        # These are the indices we will need to update
        affected = collect(bfs(grid, cur, dir))
        # Empty if we can't move in this direction
        if isempty(affected)
            continue
        end
        # Need to sort affected by negative of dir to move the furthest first
        affected = sort(affected, by=x -> -dir[1] * x[1] - dir[2] * x[2])
        for f in affected
            # Swap element with the one in the direction of dir
            f_ = f .+ dir
            t = grid[f_[1], f_[2]]
            grid[f_[1], f_[2]] = grid[f[1], f[2]]
            grid[f[1], f[2]] = t
        end

        cur = cur .+ dir
    end
    return score(grid)
end

function bfs(grid, s, d)
    explored = Set()
    unexplored = Set([s])
    while !isempty(unexplored)
        cur = pop!(unexplored)
        cur_ = cur .+ d
        if grid[cur_[1], cur_[2]] == '#'
            return Set()
        end
        if grid[cur_[1], cur_[2]] == '['
            if d[1] == 0 # moving right-left
                union!(unexplored, Set([cur_]))
            else
                union!(unexplored, Set([cur_, tuple(cur_ .+ [0, 1]...)]))
            end
        end
        if grid[cur_[1], cur_[2]] == ']'
            if d[1] == 0 # moving right-left
                union!(unexplored, Set([cur_]))
            else
                union!(unexplored, Set([cur_, tuple(cur_ .+ [0, -1]...)]))
            end
        end
        union!(explored, Set([cur]))
    end
    return explored
end

test_string_2024_15_abc = """
####################
##....[]....[]..[]##
##............[]..##
##..[][]....[]..[]##
##...[].......[]..##
##[]##....[]......##
##[]......[]..[]..##
##..[][...@.].[][]##
##........[]......##
####################

^
"""
test_string_2024_15_a = """
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<
"""
test_string_2024_15_b = """
##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^
"""
test_string_2024_15_b_end = """
##########
#.O.O.OOO#
#........#
#OO......#
#OO@.....#
#O#.....O#
#O.....OO#
#O.....OO#
#OO....OO#
##########
"""

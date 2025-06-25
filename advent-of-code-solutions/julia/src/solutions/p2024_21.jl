"""21. https://adventofcode.com/2024/day/21

This problem really challenged me. The structure involves a sequence of simple
nested path-finding problems, where the output of one level is the input of the
next. Due to this chaining, it's clear that simply finding the optimal solution
on level n would not guarantee an optimal solution on level n+1. Besides, there
are many competing optimal solutions at each level, due to the Manhattan
distance. Brute force didn't sound interesting. So I came up with some search
heuristics:

1. Avoid paths that mix together horizontal and vertical movements. Batch them
   instead, since on the next level, you can stay on A and press it a few times
   in a row.
2. Avoid going to the < key, since it's the farthest from A.
3. Avoid moves that produce < on the next level. This leads to these rules:
    a. When going from ^ to >, go down then right.
    b. When going from > to ^, go left then up.
    c. When going from v to A, go up then right.
    d. When going from A to v, go down then left.

With these heuristics, we have removed all search and choice from the problem,
once we are on the directional pad. On the numerical pad, there are few pathing
possibilities to consider, but they are no larger than 2**4. This worked well
enough with string replacement to solve part (a).

For part (b), however, the string expansion was no longer feasible. The string
length at iteration n was ~3 ** n, so after 25 iterations, it would take ~8e11
single-character bytes = 800GB of memory. I had to rewrite. The dynamic
programming structure was not intuitive to me.

The dynamic programming problem has this structure:

  expand_length[path, n] = sum(transition_length(path[i], path[i+1], n) for i in 1:length(path)-1)

  transition_length[c1, c2, n] = minimum(
        expand_length(path, n) for path in paths_between_characters_2x3(c1, c2)
    ) if n > 1,
    minimum(
        length(path) for path in paths_between_characters_2x3(c1, c2)
    ) if n == 1

  paths_between_characters_2x3[c1, c2] = paths from c1 to c2 on the directional pad

In hindsight, it's really straightforward, but I wasn't able to see it and I
needed a hint. The complexity of this approach is O(n * n * m * k), where n is
the number of buttons on the directional pad, m is the number of pad iterations,
and k is the average number of paths between two buttons. In our instance, this
is 5 * 5 * 25 * 2 = 1250, so this solution is extremely fast.
"""

const NUMERICAL_KEY_PAD::Matrix{Char} = ['7' '8' '9'; '4' '5' '6'; '1' '2' '3'; 'X' '0' 'A']
const DIRECTIONAL_KEY_PAD::Matrix{Char} = ['X' '^' 'A'; '<' 'v' '>']
# Just writing these out is simpler than coding a search algo.
# I ordered the values so the heuristically favored one is first.
const paths_between_characters_2x3 = Dict{Tuple{Char,Char},Vector{Vector{Char}}}(
    ('^', 'A') => [['>']],
    ('^', 'v') => [['v']],
    ('^', '>') => [['>', 'v'], ['v', '>']],
    ('^', '^') => [[]],
    ('^', '<') => [['v', '<']],
    ('A', 'A') => [[]],
    ('A', 'v') => [['<', 'v'], ['v', '<']],
    ('A', '>') => [['v']],
    ('A', '^') => [['<']],
    ('A', '<') => [['v', '<', '<'], ['<', 'v', '<']],
    ('>', 'A') => [['^']],
    ('>', 'v') => [['<']],
    ('>', '>') => [[]],
    ('>', '^') => [['<', '^'], ['^', '<']],
    ('>', '<') => [['<', '<']],
    ('v', 'A') => [['^', '>'], ['>', '^']],
    ('v', 'v') => [[]],
    ('v', '>') => [['>']],
    ('v', '^') => [['^']],
    ('v', '<') => [['<']],
    ('<', 'A') => [['>', '>', '^'], ['>', '^', '>']],
    ('<', 'v') => [['>']],
    ('<', '>') => [['>', '>']],
    ('<', '^') => [['>', '^']],
    ('<', '<') => [[]],
)

function solve(input::Question{2024,21,'a'})::Int
    if input.s == ""
        s = test_string_2024_21
    else
        s = input.s
    end

    # Number of directional key pads.
    n = 2
    # Parse the input
    lines = split(strip(s), '\n')

    if s == test_string_2024_21
        split_lines = [(split(line, ": ")[1], split(line, ": ")[2]) for line in lines]
        total = 0
        for (code, solution) in split_lines
            # Get the numerical key pad paths.
            paths = string_expander_4x3(['A'; code...])

            # Get the directional key pad paths.
            min_length = minimum(expand_length(path, n) for path in paths)

            # Parse the code
            score = min_length * parse(Int, code[1:3])
            solved_score = length(solution) * parse(Int, code[1:3])
            @assert(score == solved_score)
            total += score
        end
        @assert(total == 126384)
    else
        total = 0
        for code in lines
            # Get the numerical key pad paths.
            paths = string_expander_4x3(['A'; code...])

            # Iterate the directional key pad paths.
            min_length = minimum(expand_length(path, n) for path in paths)

            # Parse the code
            score = min_length * parse(Int, code[1:3])
            total += score
        end
    end
    return total
end

function string_expander_4x3(s::Vector{Char})::Vector{Vector{Char}}
    # This function only ever produces ~8 paths, so I do not optimize it with
    # pre-allocations.

    # All keypads start with an A.
    strings::Vector{Vector{Char}} = [['A']]
    for i in 1:length(s)-1
        possible_paths = paths_between_characters_4x3(s[i], s[i+1])
        new_strings = Vector{Vector{Char}}()
        for path in possible_paths
            for string in strings
                push!(new_strings, vcat(string, path))
            end
        end
        strings = new_strings
    end
    return strings
end

solution_cache_4x3 = Dict{Tuple{Char,Char},Vector{Vector{Char}}}()
function paths_between_characters_4x3(c1::Char, c2::Char)::Vector{Vector{Char}}
    # We use heuristics here to reduce the search space to two options: either
    # do all the horizontal movements first or do all the vertical movements
    # first. These paths are intuitively optimal as the allow you to press the A
    # key a few times in a row and avoid the back and forth.
    if haskey(solution_cache_4x3, (c1, c2))
        return solution_cache_4x3[(c1, c2)]
    end
    start = findfirst(==(c1), NUMERICAL_KEY_PAD)
    target = findfirst(==(c2), NUMERICAL_KEY_PAD)
    n, _ = size(NUMERICAL_KEY_PAD)

    if start[1] <= target[1]
        vert = fill('v', target[1] - start[1])
    else
        vert = fill('^', start[1] - target[1])
    end
    if start[2] <= target[2]
        hori = fill('>', target[2] - start[2])
    else
        hori = fill('<', start[2] - target[2])
    end

    # If we're in the bottom row and we need to go to the left column, we have
    # to go vertical first to avoid the missing square. Go horizontal first, if
    # this is reversed. Otherwise, return the two possibilities: horizontal
    # first and vertical first.
    out = Vector{Vector{Char}}()
    if start[2] == 1 && target[1] == n || length(hori) == 0 || length(vert) == 0
        out = push!(out, vcat(hori, vert, ['A']))
    elseif start[1] == n && target[2] == 1
        out = push!(out, vcat(vert, hori, ['A']))
    else
        out = push!(out, vcat(hori, vert, ['A']))
        out = push!(out, vcat(vert, hori, ['A']))
    end
    solution_cache_4x3[(c1, c2)] = out
    return out
end

function expand_length(sequence::Vector{Char}, levels::Int)::Int
    return sum(transition_length(sequence[i], sequence[i+1], levels) for i in 1:length(sequence)-1)
end

length_cache = Dict{Tuple{Char,Char,Int},Int}()
function transition_length(c1::Char, c2::Char, levels::Int)::Int
    if haskey(length_cache, (c1, c2, levels))
        return length_cache[(c1, c2, levels)]
    end

    paths = paths_between_characters_2x3[(c1, c2)]
    if levels == 1
        # Base case: we hit bottom and we just return the length.
        result = minimum(length([path; 'A']) for path in paths)
    else
        # Recursive case: we expand the path one level deeper.
        result = minimum(expand_length(['A'; path; 'A'], levels - 1) for path in paths)
    end

    length_cache[(c1, c2, levels)] = result
    return result
end

function solve(input::Question{2024,21,'b'})::Int
    if input.s == ""
        s = test_string_2024_21
    else
        s = input.s
    end

    # Number of directional key pads.
    n = 25
    # Parse the input
    lines::Vector{String} = split(strip(s), '\n')

    if s == test_string_2024_21
        return 0
    else
        total = 0
        for code in lines
            # Get the numerical key pad paths.
            paths = string_expander_4x3(['A'; code...])

            # Get the directional key pad paths.
            min_length = typemax(Int)
            for path in paths
                length_result = expand_length(path, n)
                min_length = min(min_length, length_result)
            end

            # Parse the code
            score = min_length * parse(Int, code[1:3])
            total += score
        end
    end
    return total
end

test_string_2024_21 = """
029A: <vA<AA>>^AvAA<^A>A<v<A>>^AvA^A<vA>^A<v<A>^A>AAvA^A<v<A>A>^AAAvA<^A>A
980A: <v<A>>^AAAvA^A<vA<AA>>^AvAA<^A>A<v<A>A>^AAAvA<^A>A<vA>^A<A>A
179A: <v<A>>^A<vA<A>>^AAvAA<^A>A<v<A>>^AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
456A: <v<A>>^AA<vA<A>>^AAvAA<^A>A<vA>^A<A>A<vA>^A<A>A<v<A>A>^AAvA<^A>A
379A: <v<A>>^AvA^A<vA<AA>>^AAvA<^A>AAvA^A<vA>^AA<A>A<v<A>A>^AAAvA<^A>A
"""
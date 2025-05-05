"""2. https://adventofcode.com/2024/day/2"""

function solve(input::Question{2024,2,'a'})
    if input.s == ""
        s = test_string_2024_02
    else
        s = input.s
    end
    s = strip(s, '\n')
    lines = [parse.(Int, split(line)) for line in split(s, '\n')]
    diffs = [diff(line) for line in lines]
    all_increasing = [all(diff .>= 0) for diff in diffs]
    all_decreasing = [all(diff .<= 0) for diff in diffs]
    changes_bounded = [all(1 .<= abs.(diff) .<= 3) for diff in diffs]
    return sum((all_increasing .| all_decreasing) .& changes_bounded)
end

function solve(input::Question{2024,2,'b'})
    if input.s == ""
        s = test_string_2024_02
    else
        s = input.s
    end
    s = strip(s, '\n')
    lines = [parse.(Int, split(line)) for line in split(s, '\n')]
    diffs = [diff(line) for line in lines]
    all_increasing = [all(diff .>= 0) for diff in diffs]
    all_decreasing = [all(diff .<= 0) for diff in diffs]
    changes_bounded = [all(1 .<= abs.(diff) .<= 3) for diff in diffs]
    valid_vector = vec((all_increasing .| all_decreasing) .& changes_bounded)
    bad_lines = lines[.!valid_vector]
    total = sum(valid_vector)
    for line in bad_lines
        for i in 1:length(line)
            new_line = vcat(line[1:i-1], line[i+1:end])
            diffs = diff(new_line)
            all_increasing = all(diffs .>= 0)
            all_decreasing = all(diffs .<= 0)
            changes_bounded = all(1 .<= abs.(diffs) .<= 3)
            if (all_increasing || all_decreasing) && changes_bounded
                total += 1
                break
            end
        end
    end
    return total
end

# Example usage
test_string_2024_02 = """
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
"""

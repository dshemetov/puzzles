"""2. https://adventofcode.com/2024/day/2"""

function solve(input::Question{2024,2,'a'})
    if input.s == ""
        s = strip(test_string_2024_02, '\n')
    else
        s = strip(input.s, '\n')
    end
    lines::Vector{Vector{Int}} = [parse.(Int, split(line, " ")) for line in split(s, "\n")]
    total::Int = 0
    for line in lines
        all_increasing::Bool = true
        all_decreasing::Bool = true
        changes_bounded::Bool = true
        for i = 1:length(line)-1
            all_increasing &= line[i] < line[i+1]
            all_decreasing &= line[i] > line[i+1]
            changes_bounded &= 1 <= abs(line[i] - line[i+1]) <= 3
            if !(all_increasing || all_decreasing) || !changes_bounded
                break
            end
        end
        total += (all_increasing || all_decreasing) && changes_bounded
    end
    return total
end

function solve(input::Question{2024,2,'b'}, method::String="method2")
    if input.s == ""
        s = strip(test_string_2024_02, '\n')
    else
        s = strip(input.s, '\n')
    end
    if method == "method1"
        return method1(s)
    elseif method == "method2"
        return method2(s)
    else
        error("Invalid method: $method")
    end
end

function method1(s::AbstractString)
    lines::Vector{Vector{Int}} = [parse.(Int, split(line, " ")) for line in split(strip(s, '\n'), "\n")]
    diffs::Vector{Vector{Int}} = [diff(line) for line in lines]
    all_increasing::Vector{Bool} = [all(diff .>= 0) for diff in diffs]
    all_decreasing::Vector{Bool} = [all(diff .<= 0) for diff in diffs]
    changes_bounded::Vector{Bool} = [all(1 .<= abs.(diff) .<= 3) for diff in diffs]
    valid_vector = vec((all_increasing .| all_decreasing) .& changes_bounded)
    bad_lines = lines[.!valid_vector]
    total = sum(valid_vector)
    for line in bad_lines
        for i in 1:length(line)
            new_line = vcat(line[1:i-1], line[i+1:end])
            diffs_new = diff(new_line)
            all_increasing_new::Bool = all(diffs_new .>= 0)
            all_decreasing_new::Bool = all(diffs_new .<= 0)
            changes_bounded_new::Bool = all(1 .<= abs.(diffs_new) .<= 3)
            if (all_increasing_new || all_decreasing_new) && changes_bounded_new
                total += 1
                break
            end
        end
    end
    return total
end


function method2(s::AbstractString)
    lines::Vector{Vector{Int}} = [parse.(Int, split(line, " ")) for line in split(strip(s, '\n'), "\n")]
    total::Int = 0
    for line in lines
        all_increasing::Bool = true
        all_decreasing::Bool = true
        changes_bounded::Bool = true
        retry::Bool = false
        for i = 1:length(line)-1
            all_increasing &= line[i] < line[i+1]
            all_decreasing &= line[i] > line[i+1]
            changes_bounded &= 1 <= abs(line[i] - line[i+1]) <= 3
            if !(all_increasing || all_decreasing) || !changes_bounded
                retry = true
                break
            end
        end
        if retry
            retry_success::Bool = false
            for j = 1:length(line)
                new_line = vcat(line[1:j-1], line[j+1:end])
                all_increasing = true
                all_decreasing = true
                changes_bounded = true
                for i = 1:length(new_line)-1
                    all_increasing &= new_line[i] < new_line[i+1]
                    all_decreasing &= new_line[i] > new_line[i+1]
                    changes_bounded &= 1 <= abs(new_line[i] - new_line[i+1]) <= 3
                    if !(all_increasing || all_decreasing) || !changes_bounded
                        break
                    end
                end
                if (all_increasing || all_decreasing) && changes_bounded
                    retry_success = true
                    break
                end
            end
        end
        total += (all_increasing || all_decreasing) && changes_bounded || retry_success
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

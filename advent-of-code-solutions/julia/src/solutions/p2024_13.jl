import LinearAlgebra: det, dot

function solve(input::Question{2024,13,'a'})
    if input.s == ""
        s = test_string_2024_13
    else
        s = input.s
    end
    s = strip(s, '\n')
    machines = split(s, "\n\n")

    total = 0
    for machine in machines
        line_a, line_b, prize = split(machine, "\n")
        button_a = [parse(Int, x.match) for x in eachmatch(r"\d+", line_a)]
        button_b = [parse(Int, x.match) for x in eachmatch(r"\d+", line_b)]
        prize = [parse(Int, x.match) for x in eachmatch(r"\d+", prize)]

        # Set up the system Ax = b
        A = [button_a[1] button_b[1]
            button_a[2] button_b[2]]
        b = prize

        # Try matrix solution first
        solution = nothing
        try
            x = inv(A) * b
            # Check if solution is valid (non-negative integers)
            if all(x .>= 0) && isapprox(x, round.(x))
                solution = convert.(Int, round.(x))
            end
        catch e
            # Matrix is singular - check if point lies on the line
            # For singular case, we need to check if the target point
            # lies on the line defined by the buttons
            if det(A) ≈ 0
                # Try different integer combinations up to reasonable bounds
                # Try using only button B
                j = prize[1] / button_b[1]
                if isinteger(j) && j >= 0 && j * button_b[2] == prize[2]
                    solution = [0, Int(j)]
                end
            end
        end

        # If we found a valid solution, calculate cost
        if solution !== nothing && all(solution .<= 100)
            total += dot([3, 1], solution)
        end
    end

    return total
end

function solve(input::Question{2024,13,'b'})
    if input.s == ""
        s = test_string_2024_13
    else
        s = input.s
    end
    s = strip(s, '\n')
    machines = split(s, "\n\n")

    total = 0
    offset = 10_000_000_000_000
    for machine in machines
        line_a, line_b, prize = split(machine, "\n")
        button_a = [parse(BigInt, x.match) for x in eachmatch(r"\d+", line_a)]
        button_b = [parse(BigInt, x.match) for x in eachmatch(r"\d+", line_b)]
        prize = [parse(BigInt, x.match) for x in eachmatch(r"\d+", prize)]

        # Set up the system Ax = b
        A = [button_a[1] button_b[1]
            button_a[2] button_b[2]]
        b = prize .+ offset

        # Try matrix solution first
        solution = nothing
        try
            x = inv(A) * b
            # Check if solution is valid (non-negative integers)
            if all(x .>= 0) && isapprox(x, round.(x))
                solution = convert.(Int, round.(x))
            end
        catch e
            # Matrix is singular - check if point lies on the line
            if det(A) ≈ 0
                # Try using only button B
                j = prize[1] / button_b[1]
                if isinteger(j) && j >= 0 && j * button_b[2] == prize[2]
                    solution = [0, Int(j)]
                end
            end
        end

        # If we found a valid solution, calculate cost
        if solution !== nothing
            total += dot([3, 1], solution)
        end
    end

    return total
end

test_string_2024_13 = """
Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279
"""

# 13. https://adventofcode.com/2024/day/13


import LinearAlgebra: det, dot

function part_a(input::AbstractString)
    s = strip(input, '\n')
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

function part_b(input::AbstractString)
    s = strip(input, '\n')
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

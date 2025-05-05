module Advent
export solve

using DataFrames
include("utils.jl")

# Dispatch to the right function by using parametric types
# https://discourse.julialang.org/t/how-to-dispatch-by-value/43266
struct Question{Y,D,P}
    s::AbstractString
end

# Include all the solution files
solution_files = readdir(joinpath(@__DIR__, "solutions"), join=true)
foreach(include, solution_files)

function do_solve(year::Int, day::Int, part::Char, test::Bool=true)
    if test
        arg = Question{year,day,part}("")
    else
        input = get_input_string(year, day)
        arg = Question{year,day,part}(input)
    end
    out = @timed solve(arg)
    return (out.value, out.time - out.compile_time)
end

function solve(year::Int, day::Int, part::Char, test::Bool=true)
    out = do_solve(year, day, part, test)
    return out
end

function solve(year::Int, day::Int, test::Bool=true)
    part1 = do_solve(year, day, 'a', test)
    part2 = do_solve(year, day, 'b', test)
    return (part1, part2)
end

function solve(year::Int, test::Bool=true)
    df = DataFrame(year=Int[], day=Int[], part=Char[], value=String[], time=Float64[])
    pattern = r"p(\d{4})_(\d{2}).jl"
    for file in solution_files
        m = match(pattern, file)
        y = parse(Int, m.captures[1])
        if year != y
            continue
        end
        day = parse(Int, m.captures[2])
        part1 = do_solve(year, day, 'a', test)
        push!(df, (year, day, 'a', part1[1], round(part1[2], digits=7)), promote=true)
        part2 = do_solve(year, day, 'b', test)
        push!(df, (year, day, 'b', part2[1], round(part2[2], digits=7)), promote=true)
    end
    # # Sort the DataFrame by year, day, and part
    # sort!(df, [:year, :day, :part])
    println(df)
    println()
    println("Total time: $(round(sum(df.time), digits=5)) seconds")
end

# solve(Question{2024,10,'a'}(""))

end

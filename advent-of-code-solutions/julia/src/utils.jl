using DotEnv
using DuckDB
using HTTP

function db_cache_write(year::Int, day::Int, input::AbstractString)
    con = DBInterface.connect(DuckDB.DB, "puzzles.db")
    # Create table if it doesn't exist
    DBInterface.execute(con, "CREATE TABLE IF NOT EXISTS inputs (year INTEGER, day INTEGER, input VARCHAR)")
    # Insert input into table
    stmt = DBInterface.prepare(con, "INSERT INTO inputs VALUES(?, ?, ?)")
    DBInterface.execute(stmt, (year, day, input))
    DBInterface.close(con)
end

function db_cache_read(year::Int, day::Int)
    con = DBInterface.connect(DuckDB.DB, "puzzles.db")
    # Create table if it doesn't exist
    DBInterface.execute(con, "CREATE TABLE IF NOT EXISTS inputs (year INTEGER, day INTEGER, input VARCHAR)")
    # Select input from table
    results = DBInterface.execute(con, "SELECT input FROM inputs WHERE year = $year AND day = $day") |> collect
    if length(results) > 0
        return results[1][1]
    end
    DBInterface.close(con)
    return nothing
end

function get_input_string(year, day)::String
    if (input = db_cache_read(year, day)) !== nothing
        return input
    end
    DotEnv.load!(".env")
    url = "https://adventofcode.com/$year/day/$day/input"
    headers = ["cookie" => """session=$(ENV["AOC_TOKEN"])"""]
    s = HTTP.request("GET", url, headers).body |> String
    db_cache_write(year, day, s)
    return s
end

function eachmatch_vector(s::AbstractString, regex::Regex)::Vector{String}
    return [m.match for m in eachmatch(regex, s)]
end

function bisect_left(arr, x; key=(x -> x))
    return searchsortedlast(arr, x, by=key)
end

function bisect_right(arr, x; key=(x -> x))
    return searchsortedfirst(arr, x, by=key)
end

function insort!(arr, x; key=(x -> x))
    insert!(arr, searchsortedfirst(arr, x, by=key), x)
end

function get_template(year, day)
    solution_template = """
"$(year). https://adventofcode.com/$year/day/$day"

function solve(input::Question{$year,$day,'a'})
    if input.s == ""
        s = test_string_$(year)_$day
    else
        s = input.s
    end
    return 0
end

function solve(input::Question{$year,$day,'b'})
    if input.s == ""
        s = test_string_$(year)_$day
    else
        s = input.s
    end
    return 0
end

test_string_$(year)_$day = ""
    """
    return solution_template
end

function write_template(year, day)
    template = get_template(year, day)
    filename = joinpath(@__DIR__, "solutions/p$(year)_$(lpad(day, 2, '0')).jl")
    open(filename, "w") do f
        write(f, template)
    end
end

function print_grid(grid)
    for row in eachrow(grid)
        println(join(row))
    end
end
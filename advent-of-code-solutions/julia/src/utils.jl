using DotEnv
using DuckDB
using HTTP

function db_make_table()
    con = DBInterface.connect(DuckDB.DB, "puzzles.db")
    DBInterface.execute(con, "CREATE TABLE IF NOT EXISTS inputs (year INTEGER, day INTEGER, input VARCHAR)")
    DBInterface.close(con)
end

function db_cache_write(year::Int, day::Int, input::AbstractString)
    con = DBInterface.connect(DuckDB.DB, "puzzles.db")
    stmt = DBInterface.prepare(con, "INSERT INTO inputs VALUES(?, ?, ?)")
    DBInterface.execute(stmt, (year, day, input))
    DBInterface.close(con)
end

function db_cache_read(year::Int, day::Int)
    con = DBInterface.connect(DuckDB.DB, "puzzles.db")
    results = DBInterface.execute(con, "SELECT input FROM inputs WHERE year = $year AND day = $day") |> collect
    if length(results) > 0
        return results[1][1]
    end
    DBInterface.close(con)
    return nothing
end

function get_input_string(year, day)
    if (input = db_cache_read(year, day)) !== nothing
        return input
    end
    DotEnv.load!(".env")
    url = "https://adventofcode.com/$year/day/$day/input"
    headers = ["cookie" => """session=$(ENV["AOC_TOKEN"])"""]
    s = HTTP.request("GET", url, headers).body |> String
    db_cache_write(year, day, s)
    s
end

function string_to_matrix(s::AbstractString, dlm=nothing)
    if dlm === nothing
        return stack([parse.(Int, collect(x)) for x in split(s, "\n")], dims=1)
    elseif dlm == ""
        return stack([parse.(Int, split(x)) for x in split(s, "\n")], dims=1)
    else
        return stack([parse.(Int, split(x, dlm)) for x in split(s, "\n")], dims=1)
    end
end

function string_to_char_matrix(s::AbstractString)
    return stack([collect(x) for x in split(s, "\n")], dims=1)
end

function eachmatch_vector(s::AbstractString, regex::Regex)
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
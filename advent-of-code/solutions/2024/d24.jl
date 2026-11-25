# 24. https://adventofcode.com/2024/day/24


function part_a(input::AbstractString)
    s = strip(input, '\n')
    init, ops = split(s, "\n\n")

    op_dag = build_op_dag(init, ops)
    zval = evaluate(op_dag)
    return parse(Int, zval, base=2)
end

function build_op_dag(init::AbstractString, ops::AbstractString)
    # Build DAG of operations or values. output => (input1, op, input2) | true | false
    op_dag = Dict{String,Union{Tuple{String,String,String},Bool}}()
    for line in split(init, "\n")
        m = match(r"(\w+): (\d)", line)
        if isnothing(m)
            error("Invalid input: $line")
        end
        op_dag[m[1]] = parse(Bool, m[2])
    end
    for line in split(ops, "\n")
        m = match(r"(\w+) (\w+) (\w+) -> (\w+)", line)
        if isnothing(m)
            error("Invalid input: $line")
        end
        op_dag[m[4]] = (string(m[1]), string(m[2]), string(m[3]))
    end
    return op_dag
end

function evaluate(op_dag::Dict{String,Union{Tuple{String,String,String},Bool}})::String
    op_dag = deepcopy(op_dag)
    # To find the value at a gate, we need to resolve the values of all its
    # parents.
    function recurse(key::String)
        if typeof(op_dag[key]) == Bool
            return op_dag[key]
        end

        a, op, b = op_dag[key]
        a_val = recurse(a)
        b_val = recurse(b)
        if op == "AND"
            out = a_val && b_val
        elseif op == "OR"
            out = a_val || b_val
        elseif op == "XOR"
            out = a_val ⊻ b_val
        else
            error("Invalid operation: $op")
        end
        op_dag[key] = out
        return out
    end

    zkeys = sort([k for k in keys(op_dag) if startswith(k, "z")], rev=true)
    zval = join(recurse.(zkeys) .|> Int, "")
    return zval
end

function part_b(input::AbstractString)
    s = strip(input, '\n')
    # init, ops = split(s, "\n\n")
    # op_dag = build_op_dag(init, ops)

    # Visualize the DAG (requires lots of extra dependencies).
    # Visualize.visualize_dag(op_dag)

    # Found the swapped wires using the DAG visualizer. Hard-coded swaps for my problem.
    # op_dag["z08"], op_dag["ffj"] = op_dag["ffj"], op_dag["z08"]
    # op_dag["z22"], op_dag["gjh"] = op_dag["gjh"], op_dag["z22"]
    # op_dag["z31"], op_dag["jdr"] = op_dag["jdr"], op_dag["z31"]
    # op_dag["dwp"], op_dag["kfm"] = op_dag["kfm"], op_dag["dwp"]

    return join(sort(["z08", "ffj", "z22", "gjh", "z31", "jdr", "dwp", "kfm"]), ",")
end

# This function is handy for finding which bits are off.
function compare_addition(op_dag::Dict{String,Union{Tuple{String,String,String},Bool}})
    zbits = evaluate(op_dag)
    zval = parse(Int, zbits, base=2)
    xkeys = sort([k for k in keys(op_dag) if startswith(k, "x")], rev=true)
    xbits = join([op_dag[x] for x in xkeys] .|> Int, "")
    xval = parse(Int, xbits, base=2)
    ykeys = sort([k for k in keys(op_dag) if startswith(k, "y")], rev=true)
    ybits = join([op_dag[y] for y in ykeys] .|> Int, "")
    yval = parse(Int, ybits, base=2)
    println("Input xval: ", xval)
    println("Input yval: ", yval)
    println("Received out binary: ", lpad(zbits, length(bitstring(xval + yval)), '0'))
    println("Expected out binary: ", bitstring(xval + yval))
    println("Received out decimal: ", zval)
    println("Expected out decimal: ", xval + yval)
end

# This function is handy for setting the x and y inputs.
function get_op_dag_with_x_y_values(op_dag::Dict{String,Union{Tuple{String,String,String},Bool}}, x_val::Int, y_val::Int)
    op_dag_with_x_y = deepcopy(op_dag)
    # LSB
    xbits = reverse(bitstring(x_val))
    ybits = reverse(bitstring(y_val))
    # LSB
    xkeys = sort([k for k in keys(op_dag) if startswith(k, "x")])
    ykeys = sort([k for k in keys(op_dag) if startswith(k, "y")])
    n = max(length(xkeys), length(ykeys))
    for i in n
        op_dag_with_x_y[xkeys[i]] = parse(Bool, xbits[i])
        op_dag_with_x_y[ykeys[i]] = parse(Bool, ybits[i])
    end
    return op_dag_with_x_y
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

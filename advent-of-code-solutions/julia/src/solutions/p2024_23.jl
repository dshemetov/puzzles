"""23. https://adventofcode.com/2024/day/23

TODO: Optimize this by using fewer dictionaries.
"""

function solve(input::Question{2024,23,'a'})
    if input.s == ""
        s = strip(test_string_2024_23, '\n')
    else
        s = strip(input.s, '\n')
    end
    s = split(s, "\n")

    # Build the network
    net = Dict{String,Vector{String}}()
    for line in s
        a, b = split(line, "-")
        if !haskey(net, a)
            net[a] = []
        end
        push!(net[a], b)
        if !haskey(net, b)
            net[b] = []
        end
        push!(net[b], a)
    end

    # Find groups of three mutually connected nodes
    groups = Set{Tuple{String,String,String}}()
    for n1 in keys(net)
        for n2 in keys(net)
            if n1 == n2
                continue
            end
            n1_neighbors = Set(net[n1])
            n2_neighbors = Set(net[n2])
            if !(n1 in n2_neighbors) || !(n2 in n1_neighbors)
                continue
            end
            n1_n2_neighbors = n1_neighbors ∩ n2_neighbors
            for n3 in n1_n2_neighbors
                if n3 == n1 || n3 == n2
                    continue
                end
                group = tuple(sort([n1, n2, n3])...)
                push!(groups, group)
            end
        end
    end

    # Filter to only groups that have a node starting with 't'
    groups = filter(g -> any(startswith.(g, "t")), groups)

    return length(groups)
end

function solve(input::Question{2024,23,'b'})
    if input.s == ""
        s = strip(test_string_2024_23, '\n')
    else
        s = strip(input.s, '\n')
    end
    s = split(s, "\n")

    # Build the network
    net = Dict{String,Vector{String}}()
    for line in s
        a, b = split(line, "-")
        if !haskey(net, a)
            net[a] = []
        end
        push!(net[a], b)
        if !haskey(net, b)
            net[b] = []
        end
        push!(net[b], a)
    end

    # Recursively find the largest fully connected subgraph
    memo = Dict{Tuple{Vector{String},Vector{String}},Vector{String}}()
    function recurse(subgraph::Vector{String}, frontier::Vector{String})::Vector{String}
        if haskey(memo, (subgraph, frontier))
            return memo[(subgraph, frontier)]
        end

        # Base case: no more nodes to add.
        if length(frontier) == 0
            return sort(subgraph)
        end

        # Store all the possible subgraphs that can be made by adding a node
        # from the frontier to the subgraph.
        sg::Vector{Vector{String}} = []
        # For every node in the frontier, add it to the subgraph and recurse.
        for n in frontier
            # If the current subgraph is not contained in the neighbors of this
            # node, then adding it will break the fully connected condition.
            if !(subgraph ⊆ net[n])
                continue
            end
            # Otherwise, add this node to the neighborhood, shrink the frontier,
            # and recurse.
            new_subgraph = sort(subgraph ∪ [n])
            new_frontier = sort(frontier ∩ net[n])
            push!(sg, recurse(new_subgraph, new_frontier))
        end

        # Return the largest subgraph.
        largest_subgraph = sg[argmax(length.(sg))]
        memo[(subgraph, frontier)] = largest_subgraph
        return largest_subgraph
    end

    d = Dict{String,Vector{String}}()
    max_size = 0
    max_size_key = ""
    for x in keys(net)
        d[x] = recurse([x], sort(net[x]))
        subgraph_size = length(d[x])
        if subgraph_size > max_size
            max_size = subgraph_size
            max_size_key = x
        end
    end

    return join(sort(d[max_size_key]), ",")
end

test_string_2024_23 = """
kh-tc
qp-kh
de-cg
ka-co
yn-aq
qp-ub
cg-tb
vc-aq
tb-ka
wh-tc
yn-cg
kh-ub
ta-co
de-co
tc-td
tb-wq
wh-td
ta-ka
td-qp
aq-cg
wq-ub
ub-vc
de-ta
wq-aq
wq-vc
wh-yn
ka-de
kh-ta
co-tc
wh-qp
tb-vc
td-yn
"""
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
    net = Dict{Int,Set{Int}}()
    for line in s
        a, b = split(line, "-")
        if !haskey(net, ix(a[1], a[2]))
            net[ix(a[1], a[2])] = Set{Int}()
        end
        push!(net[ix(a[1], a[2])], ix(b[1], b[2]))
        if !haskey(net, ix(b[1], b[2]))
            net[ix(b[1], b[2])] = Set{Int}()
        end
        push!(net[ix(b[1], b[2])], ix(a[1], a[2]))
    end

    # Find groups of three mutually connected nodes
    groups = Set{Tuple{Int,Int,Int}}()
    for n1 in keys(net)
        for n2 in keys(net)
            # Filter out nodes that don't start with 't'
            if n1 == n2
                continue
            end
            n1_neighbors = net[n1]
            n2_neighbors = net[n2]
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

    groups = filter(g -> any(ix('t', 'a') .<= g .<= ix('t', 'z')), groups)

    return length(groups)
end

function ix(c1::Char, c2::Char)::Int
    return (Int(c1) - Int('a') + 1) * 26 + (Int(c2) - Int('a') + 1)
end

function inv_ix(ix::Int)::Tuple{Char,Char}
    return (Char(div(ix - 1, 26) + Int('a') - 1), Char((ix - 1) % 26 + Int('a')))
end

function solve(input::Question{2024,23,'b'})
    if input.s == ""
        s = strip(test_string_2024_23, '\n')
    else
        s = strip(input.s, '\n')
    end
    s = split(s, "\n")

    # Build the network
    net = Dict{Int,BitSet}()
    for line in s
        a, b = split(line, "-")
        ka, kb = ix(a[1], a[2]), ix(b[1], b[2])
        if !haskey(net, ka)
            net[ka] = BitSet()
        end
        push!(net[ka], kb)
        if !haskey(net, kb)
            net[kb] = BitSet()
        end
        push!(net[kb], ka)
    end

    d = Dict{Int,BitSet}()
    max_size = 0
    max_size_key = 0
    # Recursively find the largest fully connected subgraph
    memo = Dict{Tuple{BitSet,BitSet,BitSet},BitSet}()
    function recurse(subgraph::BitSet, frontier::BitSet, excluded::BitSet)::BitSet
        if haskey(memo, (subgraph, frontier, excluded))
            return memo[(subgraph, frontier, excluded)]
        end

        # Early exit
        if length(frontier) + length(subgraph) < max_size
            return subgraph
        end

        # Base case: no more nodes to add.
        if length(frontier) == 0
            return subgraph
        end

        # Store all the possible subgraphs that can be made by adding a node
        # from the frontier to the subgraph.
        sg = BitSet[]
        frontier_copy = copy(frontier)
        # For every node in the frontier, add it to the subgraph and recurse.
        for n in frontier_copy
            # If the current subgraph is not contained in the neighbors of this
            # node, then adding it will break the fully connected condition.
            if !(subgraph ⊆ net[n])
                # Move n from frontier to excluded
                delete!(frontier, n)
                push!(excluded, n)
                continue
            end
            # Otherwise, add this node to the neighborhood, shrink the frontier,
            # and recurse.
            new_subgraph = subgraph ∪ BitSet([n])
            new_frontier = frontier ∩ net[n]
            new_excluded = excluded ∩ net[n]
            push!(sg, recurse(new_subgraph, new_frontier, new_excluded))

            # Move n from frontier to excluded
            delete!(frontier, n)
            push!(excluded, n)
        end

        # Return the largest subgraph.
        largest_subgraph = length(sg) > 0 ? sg[argmax(length.(sg))] : subgraph
        memo[(subgraph, frontier, excluded)] = largest_subgraph
        return largest_subgraph
    end

    for x in keys(net)
        d[x] = recurse(BitSet([x]), BitSet(net[x]), BitSet())
        subgraph_size = length(d[x])
        if subgraph_size > max_size
            max_size = subgraph_size
            max_size_key = x
        end
    end

    # Get characters back.
    return join(sort([inv_ix(x) for x in d[max_size_key]]), "-")
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
"""23. https://adventofcode.com/2024/day/23"""


def ix(c1: str, c2: str) -> int:
    """Convert two characters to an integer index."""
    return (ord(c1) - ord("a") + 1) * 26 + (ord(c2) - ord("a") + 1)


def inv_ix(ix: int) -> tuple[str, str]:
    """Convert integer index back to character pair."""
    return (chr((ix - 1) // 26 + ord("a") - 1), chr((ix - 1) % 26 + ord("a")))


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    7
    """
    s = s.strip("\n")
    lines = s.split("\n")

    # Build the network
    net = {}
    for line in lines:
        a, b = line.split("-")
        ka = ix(a[0], a[1])
        kb = ix(b[0], b[1])

        if ka not in net:
            net[ka] = set()
        net[ka].add(kb)

        if kb not in net:
            net[kb] = set()
        net[kb].add(ka)

    # Find groups of three mutually connected nodes
    groups = set()
    for n1 in net:
        for n2 in net:
            if n1 == n2:
                continue
            n1_neighbors = net[n1]
            n2_neighbors = net[n2]
            if n1 not in n2_neighbors or n2 not in n1_neighbors:
                continue
            n1_n2_neighbors = n1_neighbors & n2_neighbors
            for n3 in n1_n2_neighbors:
                if n3 == n1 or n3 == n2:
                    continue
                group = tuple(sorted([n1, n2, n3]))
                groups.add(group)

    # Filter groups to only include nodes that start with 't'
    filtered_groups = set()
    for group in groups:
        if any(ix("t", "a") <= g <= ix("t", "z") for g in group):
            filtered_groups.add(group)

    return len(filtered_groups)


def solve_b(s: str) -> str:
    """
    Examples:
    >>> solve_b(test_string)
    "('c', 'o')-('d', 'e')-('k', 'a')-('t', 'a')"
    """
    s = s.strip("\n")
    lines = s.split("\n")

    # Build the network
    net = {}
    for line in lines:
        a, b = line.split("-")
        ka, kb = ix(a[0], a[1]), ix(b[0], b[1])
        if ka not in net:
            net[ka] = set()
        net[ka].add(kb)
        if kb not in net:
            net[kb] = set()
        net[kb].add(ka)

    # Recursively find the largest fully connected subgraph
    memo = {}
    max_size = 0
    max_size_key = 0

    def recurse(subgraph: set, frontier: set, excluded: set) -> set:
        key = (frozenset(subgraph), frozenset(frontier), frozenset(excluded))
        if key in memo:
            return memo[key]

        # Early exit
        if len(frontier) + len(subgraph) < max_size:
            return subgraph

        # Base case: no more nodes to add
        if len(frontier) == 0:
            return subgraph

        # Store all the possible subgraphs that can be made by adding a node
        # from the frontier to the subgraph
        sg = []
        frontier_copy = frontier.copy()

        # For every node in the frontier, add it to the subgraph and recurse
        for n in frontier_copy:
            # If the current subgraph is not contained in the neighbors of this
            # node, then adding it will break the fully connected condition
            if not subgraph.issubset(net[n]):
                # Move n from frontier to excluded
                frontier.remove(n)
                excluded.add(n)
                continue

            # Otherwise, add this node to the neighborhood, shrink the frontier,
            # and recurse
            new_subgraph = subgraph | {n}
            new_frontier = frontier & net[n]
            new_excluded = excluded & net[n]
            sg.append(recurse(new_subgraph, new_frontier, new_excluded))

            # Move n from frontier to excluded
            frontier.remove(n)
            excluded.add(n)

        # Return the largest subgraph
        largest_subgraph = max(sg, key=len) if sg else subgraph
        memo[key] = largest_subgraph
        return largest_subgraph

    for x in net:
        d = recurse({x}, net[x].copy(), set())
        subgraph_size = len(d)
        if subgraph_size > max_size:
            max_size = subgraph_size
            max_size_key = x

    # Get the largest subgraph and convert back to characters
    largest_subgraph = recurse({max_size_key}, net[max_size_key].copy(), set())
    result = [inv_ix(x) for x in largest_subgraph]
    result.sort()

    return "-".join([f"('{c1}', '{c2}')" for c1, c2 in result])


test_string = """kh-tc
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

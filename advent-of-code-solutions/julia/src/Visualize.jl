module Visualize

using GraphMakie, CairoMakie, Graphs, NetworkLayout
export visualize_dag

function visualize_dag(op_dag::Dict{String,Union{Tuple{String,String,String},Bool}};
    filename="dag_visualization.png")
    # Create mapping from node names to indices
    all_nodes = collect(keys(op_dag))
    node_to_idx = Dict(node => i for (i, node) in enumerate(all_nodes))
    n_nodes = length(all_nodes)

    # Build the graph
    g = SimpleDiGraph(n_nodes)
    edge_count = 0

    # Add edges based on dependencies
    for (output_node, value) in op_dag
        if isa(value, Tuple)  # This is a logic gate
            input1, _, input2 = value  # We don't need the operation for graph construction
            # Add edges from inputs to output
            if haskey(node_to_idx, input1) && haskey(node_to_idx, output_node)
                add_edge!(g, node_to_idx[input1], node_to_idx[output_node])
                edge_count += 1
            end
            if haskey(node_to_idx, input2) && haskey(node_to_idx, output_node)
                add_edge!(g, node_to_idx[input2], node_to_idx[output_node])
                edge_count += 1
            end
        end
    end

    println("Graph built: $(n_nodes) nodes, $(edge_count) edges")
    println("Actual edges in graph: $(ne(g))")

    # Categorize nodes for coloring, labeling, and shapes
    node_colors = []
    node_labels = []
    node_shapes = []

    for node in all_nodes
        if startswith(node, "x") || startswith(node, "y")
            # Input nodes - green circles
            push!(node_colors, :green)
            value = op_dag[node]
            push!(node_labels, "$node\n($value)")
            push!(node_shapes, :circle)
        elseif startswith(node, "z")
            # Output nodes - red, shape based on operation
            operation = op_dag[node][2]
            push!(node_colors, :red)
            push!(node_labels, "$node\n($operation)")
            if operation == "AND"
                push!(node_shapes, :utriangle)  # triangle for AND
            elseif operation == "OR"
                push!(node_shapes, :circle)     # circle for OR
            elseif operation == "XOR"
                push!(node_shapes, :rect)       # square for XOR
            else
                push!(node_shapes, :circle)
            end
        else
            # Logic gate nodes - color and shape by operation type
            if isa(op_dag[node], Tuple)
                _, operation, _ = op_dag[node]
                if operation == "AND"
                    push!(node_colors, :blue)
                    push!(node_shapes, :utriangle)  # triangle for AND
                elseif operation == "OR"
                    push!(node_colors, :orange)
                    push!(node_shapes, :circle)     # circle for OR
                elseif operation == "XOR"
                    push!(node_colors, :purple)
                    push!(node_shapes, :rect)       # square for XOR
                else
                    push!(node_colors, :gray)
                    push!(node_shapes, :circle)
                end
                push!(node_labels, "$node\n($operation)")
            else
                push!(node_colors, :gray)
                push!(node_labels, node)
                push!(node_shapes, :circle)
            end
        end
    end

    # Use CairoMakie for high-resolution static output
    CairoMakie.activate!()

    # Create ultra-high resolution figure
    fig = Figure(size=(4200, 3000), fontsize=20)
    ax = Axis(fig[1, 1], title="Logic Gate DAG Visualization")

    # Use Stress layout for hierarchical DAG visualization
    layout = Stress(iterations=500)

    # Create the graph plot
    graphplot!(ax, g,
        layout=layout,
        node_color=node_colors,
        node_marker=node_shapes,
        node_size=50,
        arrow_size=20,
        arrow_show=true,
        edge_width=2,
        edge_color=:black,
        nlabels=node_labels,
        nlabels_textsize=11,
        nlabels_color=:black,
        nlabels_align=(:center, :center),
        node_attr=(; strokewidth=2, strokecolor=:black))

    # Add legend
    legend_elements = [
        MarkerElement(color=:green, marker=:circle),
        MarkerElement(color=:red, marker=:circle),
        MarkerElement(color=:blue, marker=:utriangle),
        MarkerElement(color=:orange, marker=:circle),
        MarkerElement(color=:purple, marker=:rect)
    ]
    legend_labels = ["Input (x/y)", "Output (z)", "AND (△)", "OR (●)", "XOR (■)"]

    Legend(fig[1, 2], legend_elements, legend_labels, "Node Types")

    # Make axes invisible since we're showing a graph
    hidedecorations!(ax)
    hidespines!(ax)

    # Save as ultra-high-resolution PNG
    png_filename = replace(filename, ".html" => ".png")
    save(png_filename, fig, px_per_unit=3)
    println("Ultra-high-resolution PNG saved as: $png_filename")

    return fig
end

end
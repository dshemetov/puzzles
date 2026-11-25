# /// script
# requires-python = ">=3.14"
# dependencies = ["networkx", "matplotlib"]
# ///
"""Draw the 2024 day 24 logic circuit as a layered graph, one column per dependency depth.

Usage: uv run tools/viz_d24.py inputs/2024/24.txt [out.png]
"""

import re
import sys

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx

# Gate type -> (colour, marker, legend text). Input and output wires are coloured by name.
GATES = {
    "AND": ("tab:blue", "^", "AND (triangle)"),
    "OR": ("tab:orange", "o", "OR (circle)"),
    "XOR": ("tab:purple", "s", "XOR (square)"),
}


def parse(text: str) -> tuple[dict[str, int], dict[str, tuple[str, str, str]]]:
    wires, gates = text.strip().split("\n\n")
    values = {name: int(v) for name, v in re.findall(r"(\w+): (\d)", wires)}
    ops = {out: (a, op, b) for a, op, b, out in re.findall(r"(\w+) (\w+) (\w+) -> (\w+)", gates)}
    return values, ops


def build_graph(values, ops) -> nx.DiGraph:
    g = nx.DiGraph()
    g.add_nodes_from(values)
    for out, (a, op, b) in ops.items():
        g.add_node(out, op=op)
        g.add_edge(a, out)
        g.add_edge(b, out)
    return g


def place(g: nx.DiGraph) -> dict[str, tuple[float, float]]:
    """One column per bit position (a ripple-carry adder has one stage per bit), rows by dependency.

    A gate's bit is the one in its input/output wire names, else the highest bit among its parents.
    Its row is one below its parents in the same column. A swapped wire shows up as an edge that
    jumps to the wrong column or row.
    """
    bit: dict[str, int] = {}
    row: dict[str, int] = {}
    for n in nx.topological_sort(g):
        parents = list(g.predecessors(n))
        if n[0] in "xyz":
            bit[n] = int(n[1:])
        elif any(p[0] in "xy" for p in parents):
            bit[n] = max(bit[p] for p in parents if p[0] in "xy")
        else:
            bit[n] = max(bit[p] for p in parents)
        same = [row[p] for p in parents if bit[p] == bit[n]]
        row[n] = 1 + max(same) if same else (0 if not parents else 1)
    cells: dict[tuple[int, int], list[str]] = {}
    for n in g:
        cells.setdefault((bit[n], row[n]), []).append(n)
    pos = {}
    for (b, r), nodes in cells.items():
        for k, n in enumerate(sorted(nodes)):
            pos[n] = (b + 0.25 * (k - (len(nodes) - 1) / 2), -r)
    return pos


def style(g: nx.DiGraph, node: str) -> tuple[str, str]:
    if node[0] in "xy":
        return "tab:green", "o"
    colour, marker, _ = GATES[g.nodes[node]["op"]]
    return ("tab:red" if node[0] == "z" else colour), marker


def main(path: str, out: str = "dag_visualization.png") -> None:
    values, ops = parse(open(path).read())
    g = build_graph(values, ops)
    print(f"Graph built: {g.number_of_nodes()} nodes, {g.number_of_edges()} edges")

    pos = place(g)
    fig, ax = plt.subplots(figsize=(60, 14))
    nx.draw_networkx_edges(g, pos, ax=ax, arrows=True, arrowsize=10, width=1, node_size=700, alpha=0.5)
    for marker in ("o", "^", "s"):
        nodes = [n for n in g if style(g, n)[1] == marker]
        nx.draw_networkx_nodes(
            g, pos, nodelist=nodes, node_shape=marker, node_size=700, ax=ax,
            node_color=[style(g, n)[0] for n in nodes], edgecolors="black", linewidths=1.5,
        )
    labels = {n: f"{n}\n({values[n]})" if n in values else f"{n}\n{g.nodes[n]['op']}" for n in g}
    nx.draw_networkx_labels(g, pos, labels=labels, font_size=7, ax=ax)

    handles = [plt.Line2D([], [], marker="o", color="tab:green", linestyle="", label="Input (x/y)"),
               plt.Line2D([], [], marker="o", color="tab:red", linestyle="", label="Output (z)")]
    handles += [plt.Line2D([], [], marker=m, color=c, linestyle="", label=text) for c, m, text in GATES.values()]
    ax.legend(handles=handles, title="Node types", loc="upper right")
    ax.set_title("Logic gate DAG, one column per bit")
    ax.axis("off")
    fig.savefig(out, dpi=100, bbox_inches="tight")
    print(f"Saved {out}")


if __name__ == "__main__":
    main(*sys.argv[1:3])

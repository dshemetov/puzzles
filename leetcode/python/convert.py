"""
Convert between a monofile and a multifile for LeetCode problems.

Automating indecision by learning about the ast module

    https://docs.python.org/3/library/ast.html#ast-helpers
"""

import ast
import re
import subprocess
from pathlib import Path

import typer

app = typer.Typer(name="LeetCode Solution Converter", chain=True)
PATH_TO_PROBLEMS_FILE = Path(__file__).parent / "problems.py"
PATH_TO_PROBLEMS = Path(__file__).parent / "problems"


@app.command("to-monofile")
def convert_to_monofile() -> None:
    """Convert a multifile to a monofile.

    Currently just stitches together all the files in the problems directory.
    """
    monofile_docstring = """
\"\"\"
Python solutions to LeetCode problems.

Keeping it as a monofile because there's something funny about it.
\"\"\"
    """
    with PATH_TO_PROBLEMS_FILE.open("w") as f:
        f.write(monofile_docstring)
        for file in sorted(PATH_TO_PROBLEMS.glob("*.py")):
            f.write("\n\n")
            f.write(file.read_text())


def _collect_names(nodes: list[ast.AST]) -> set[str]:
    """Collect all names referenced in a list of AST nodes."""
    names: set[str] = set()
    for node in nodes:
        for child in ast.walk(node):
            if isinstance(child, ast.Name):
                names.add(child.id)
            elif isinstance(child, ast.Attribute):
                # Only the root name binds to an import (e.g. `np` in `np.array`)
                root = child.value
                while isinstance(root, ast.Attribute):
                    root = root.value
                if isinstance(root, ast.Name):
                    names.add(root.id)
    return names


def _filter_imports(import_nodes: list[ast.AST], used_names: set[str]) -> list[ast.AST]:
    """Return only import nodes that export a name referenced in used_names."""
    result = []
    for node in import_nodes:
        if isinstance(node, ast.Import):
            for alias in node.names:
                bound = alias.asname or alias.name.split(".")[0]
                if bound in used_names:
                    result.append(node)
                    break
        elif isinstance(node, ast.ImportFrom):
            for alias in node.names:
                bound = alias.asname or alias.name
                if bound in used_names:
                    result.append(node)
                    break
    return result


def _build_helper_index(helper_nodes: list[ast.AST]) -> dict[str, ast.AST]:
    """Map defined names to the helper node that defines them."""
    index: dict[str, ast.AST] = {}
    for node in helper_nodes:
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            index[node.name] = node
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    index[target.id] = node
    return index


def _resolve_helpers(
    problem_node: ast.AST,
    helper_by_name: dict[str, ast.AST],
    all_helpers: list[ast.AST],
) -> list[ast.AST]:
    """Return helpers transitively needed by problem_node, in original source order."""
    needed_ids: set[int] = set()
    visited: set[str] = set()
    queue = list(_collect_names([problem_node]) & helper_by_name.keys())

    while queue:
        name = queue.pop()
        if name in visited:
            continue
        visited.add(name)
        helper = helper_by_name[name]
        needed_ids.add(id(helper))
        for dep in _collect_names([helper]) & helper_by_name.keys():
            if dep not in visited:
                queue.append(dep)

    return [h for h in all_helpers if id(h) in needed_ids]


def _source_for_node(source_lines: list[str], node: ast.AST) -> str:
    """Return original source for a node using its line numbers."""
    return "\n".join(source_lines[node.lineno - 1 : node.end_lineno])


def _source_with_leading_comments(source_lines: list[str], node: ast.AST, search_from: int) -> str:
    """Like _source_for_node, but also pulls in comment lines directly above the node."""
    node_start = node.lineno - 1  # 0-indexed

    leading_start = node_start
    for i in range(node_start - 1, search_from - 1, -1):
        stripped = source_lines[i].strip()
        if stripped.startswith("#"):
            leading_start = i
        else:
            break  # stop at blank lines or real code

    return "\n".join(source_lines[leading_start : node.end_lineno])


@app.command("to-multifile")
def convert_to_multifile() -> None:
    """Convert a monofile to a multifile."""
    source = PATH_TO_PROBLEMS_FILE.read_text()
    source_lines = source.splitlines()
    tree = ast.parse(source)

    import_nodes: list[ast.AST] = []
    helper_nodes: list[ast.AST] = []
    problem_nodes: list[ast.FunctionDef] = []

    for x in tree.body[1:]:  # skip module docstring
        if isinstance(x, (ast.Import, ast.ImportFrom)):
            import_nodes.append(x)
        elif isinstance(x, ast.FunctionDef) and re.match(r"p(\d+)", x.name):
            problem_nodes.append(x)
        else:
            helper_nodes.append(x)

    # Precompute the end-line of each node's predecessor in the original file,
    # so _source_with_leading_comments knows how far back to scan.
    node_prev_end: dict[int, int] = {}
    prev_end = 0
    for node in tree.body[1:]:
        node_prev_end[id(node)] = prev_end
        prev_end = node.end_lineno

    helper_by_name = _build_helper_index(helper_nodes)

    PATH_TO_PROBLEMS.mkdir(exist_ok=True)

    for problem_node in problem_nodes:
        needed_helpers = _resolve_helpers(problem_node, helper_by_name, helper_nodes)
        all_chunk_nodes: list[ast.AST] = [*needed_helpers, problem_node]

        used_names = _collect_names(all_chunk_nodes)
        filtered_imports = _filter_imports(import_nodes, used_names)

        import_text = "\n".join(_source_for_node(source_lines, node) for node in filtered_imports)
        chunk_parts = [
            _source_with_leading_comments(source_lines, node, node_prev_end[id(node)]) for node in all_chunk_nodes
        ]
        problem_text = "\n\n".join(chunk_parts)
        problem_number = re.search(r"p(\d+)", problem_node.name).group(1)

        problem_file = PATH_TO_PROBLEMS / f"p{int(problem_number):04d}.py"
        with problem_file.open("w") as f:
            f.write(import_text)
            f.write("\n\n")
            f.write(problem_text)
            f.write("\n")


def _problem_number(node: ast.AST) -> int:
    if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
        m = re.match(r"p(\d+)", node.name)
        if m:
            return int(m.group(1))
    return -1


@app.command("sort")
def sort_problems() -> None:
    """Sort problem functions/classes in problems.py by problem number, helpers first."""
    source = PATH_TO_PROBLEMS_FILE.read_text()
    source_lines = source.splitlines()
    tree = ast.parse(source)

    docstring_node = tree.body[0]
    import_nodes: list[ast.AST] = []
    helper_nodes: list[ast.AST] = []
    problem_nodes: list[ast.AST] = []

    for node in tree.body[1:]:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            import_nodes.append(node)
        elif _problem_number(node) >= 0:
            problem_nodes.append(node)
        else:
            helper_nodes.append(node)

    problem_nodes.sort(key=_problem_number)

    parts: list[str] = []
    parts.append(_source_for_node(source_lines, docstring_node))
    parts.append("\n".join(_source_for_node(source_lines, n) for n in import_nodes))
    for node in helper_nodes:
        parts.append(_source_for_node(source_lines, node))
    for node in problem_nodes:
        parts.append(_source_for_node(source_lines, node))

    PATH_TO_PROBLEMS_FILE.write_text("\n\n".join(parts) + "\n")
    typer.echo(f"Sorted {len(problem_nodes)} problems, {len(helper_nodes)} helpers.")

    subprocess.run(
        ["uv", "tool", "run", "ruff", "check", "--select", "I", "--fix", str(PATH_TO_PROBLEMS_FILE)], check=True
    )
    subprocess.run(["uv", "tool", "run", "ruff", "format", str(PATH_TO_PROBLEMS_FILE)], check=True)


if __name__ == "__main__":
    app()

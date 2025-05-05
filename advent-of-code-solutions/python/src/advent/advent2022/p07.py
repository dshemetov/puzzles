"""No Space Left On Device
https://adventofcode.com/2022/day/7
"""

import re


def print_dirs(dirs: dict, dir: str, indent: int = 0):
    print(" " * 2 * indent + " - " + dir)
    for child in dirs[dir]:
        if isinstance(child, str) and child.endswith("/"):
            print_dirs(dirs, child, indent + 1)
        else:
            print(" " * (2 * indent + 3) + child + " " + str(dirs[child]))


def get_dirs(s: str) -> tuple[dict, dict]:
    dir_map: dict[str, list[str]] = {"/": []}
    dir_size: dict[str, int] = {}
    cur_path = "/"
    r = re.compile(r"(\d+) ([a-zA-Z0-9\.]+)")  # e.g. 14848514 b.txt

    for line in s.split("\n"):
        if not line:
            continue
        elif line.startswith("$ cd "):
            new_dir = line[5:]
            if new_dir == "..":
                new_path = cur_path[: cur_path[:-1].rfind("/") + 1]
            else:
                if new_dir == "/":
                    new_path = "/"
                else:
                    new_path = cur_path + new_dir + "/"

            if new_path not in dir_map:
                dir_map[cur_path].append(new_path)
                dir_map[new_path] = []
            cur_path = new_path
        elif line.startswith("$ ls"):
            continue
        elif line.startswith("dir "):
            new_path = cur_path + line[4:] + "/"
            if new_path not in dir_map:
                dir_map[cur_path].append(new_path)
                dir_map[new_path] = []
        else:
            num, name = r.findall(line)[0]
            dir_map[cur_path].append(cur_path + name)
            dir_size[cur_path + name] = int(num)

    return dir_map, dir_size


def get_dir_sizes(s: str) -> dict:
    dir_map, dir_sizes = get_dirs(s)

    stack: list[tuple[str, bool]] = [("/", False)]
    while stack:
        cur_dir, visited = stack.pop()
        if visited:
            dir_sizes[cur_dir] = sum(dir_sizes[child] for child in dir_map[cur_dir])
        else:
            stack.append((cur_dir, True))
            stack.extend((child, False) for child in dir_map[cur_dir] if child.endswith("/"))

    return dir_sizes


def solve_a(s: str) -> int:
    """
    Examples:
    >>> solve_a(test_string)
    95437
    """
    s = s.strip("\n")
    dir_sizes = get_dir_sizes(s)
    return sum(size for key, size in dir_sizes.items() if key.endswith("/") and size <= 100000)


def solve_b(s: str) -> int:
    """
    Examples:
    >>> solve_b(test_string)
    24933642
    """
    s = s.strip("\n")
    dir_sizes = get_dir_sizes(s)
    space_needed = 30_000_000 - (70_000_000 - dir_sizes["/"])
    return min(size for key, size in dir_sizes.items() if key.endswith("/") and size >= space_needed)


test_string = """
$ cd /
$ ls
dir a
14848514 b.txt
8504156 c.dat
dir d
$ cd a
$ ls
dir e
29116 f
2557 g
62596 h.lst
$ cd e
$ ls
584 i
$ cd ..
$ cd ..
$ cd d
$ ls
4060174 j
8033020 d.log
5626152 d.ext
7214296 k
"""

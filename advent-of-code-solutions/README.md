# Advent of Code Solutions

[Advent of Code](https://adventofcode.com/) is a great set of Christmas-themed coding challenges.

## Python Usage

Commands expected to be run in the `python` directory.

```sh
# Install uv (Linux/MacOS)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Install Python, venv, and dependencies
uv sync

# Alias the run command for convenience
alias advent="uv run python -m advent"

# Set AoC cookie in .env
advent set-cookie

# Print the answer to puzzle 2021 day 2 part b
advent solve -y 2021 -d 2 -p b

# Print the answer to current year's day 2 (both parts)
advent solve -d 21

# Clear cached answer and solve again
advent solve -y 2021 -d 2 -c

# See help for more
advent solve --help
```

## Julia Usage

Open the Julia REPL in the `julia` directory and run the following commands.

```julia
# Install dependencies
using Pkg
Pkg.activate(".")
Pkg.instantiate()

# Run the test case for 2024 day 2 part b
using Advent
Advent.solve(2024, 2, 'b')

# Get the actual solutions for every 2024 problem
Advent.solve(2024, false)
```

## Stats

TODO.

## Background

I first got into Advent of Code over the 2015 Christmas holiday with my friend Evin at his family home in LA.
After a few days of only playing SSX Tricky and drinking peppermint schnapps, we were ready to re-engage our brains.
Evin got functional with JavaScript and I was just getting started with Python.
Doing puzzles while cozy with friends is one of my favorite things to do.

- AoC 2024: 7/50 Python, a few in Julia.
- AoC 2023: 7/50 Python.
- AoC 2022: 12/50 Python (with Numba and Cython).
- AoC 2021: 43/50 Python.
- AoC 2020: 32/50 Python.
- AoC 2019: 4/50 Python, ??/50 Mathematica.
- AoC 2018: 13/50 Mathematica. Lessons learned:
  - Mathematica has a some really cool builtin functions (e.g. see the three-line solution to Day 6 with [DistanceMatrix](https://reference.wolfram.com/language/ref/DistanceMatrix.html) and [Nearest](https://reference.wolfram.com/language/ref/Nearest.html)).
  - Even though Mathematica has fast built-ins, Python can be faster for simple for-loops (e.g. see Day 9 and the attached Python solution). I did not have the courage to try to implement a linked-list in Mathematica for Day 9.
  - Mathematica notebooks don't look great on GitHub.
  - Mathematica [doesn't support lazy iteration natively](https://mathematica.stackexchange.com/questions/226334/breaking-functional-loops-and-doing-lazy-evaluation-in-mathematica).
  - Mathematica doesn't make it easy to make new data structures (though [these are nice to have](https://reference.wolfram.com/language/guide/DataStructures.html)).
  - Mathematica debugging isn't easy (and it isn't easy to switch from developing code in a Notebook to Eclipse, where they maintain a debugger plugin).
- AoC 2015: 6/50 Python.

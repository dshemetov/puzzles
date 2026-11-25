# SBCL vs Python on AoC 2024, days 1-10

> **Layout note.** These measurements were taken with the earlier in-process runner (all solutions
> loaded into one process, compiled files cached). The solutions have since become standalone
> scripts, `solutions/2024/dNN.{ext}`, each started in its own process with `just lang=... run`, so
> startup and compile time now show up per run. The algorithm comparisons still hold; the
> `run.lisp` and `just test` commands mentioned below no longer exist (`just check 2024` replaces them).

The solutions in `solutions/2024/d*.lisp` transliterate the Python in
`solutions/2024/d*.py`, the same way `solutions/2024/d*.nu` does. Running
identical algorithms in all three places gives a clean read on where each
language lands.

## Method

- Inputs are the real puzzle inputs, cached in `inputs/2024/` (copied from the Rust cache).
- Both sides are measured **compute only**, with the code already compiled and
  the input already read. Python gets a warm-up call first so numba's JIT and
  its on-disk cache are not counted.
- Best of 3 runs per part.
- Every answer was checked against the Python answer on the real input and
  against the puzzle example: `just test` runs all 40 checks.

## No libraries

Everything runs on a bare `sbcl` with no quicklisp and no dependencies. The one
place that costs something is regular expressions, which Common Lisp does not
have in the standard: the `parse-ints` helper scans runs of digits by hand, and day 3 walks
the string looking for `mul(`, `do()` and `don't()` itself.

## Where the transliteration deviates

Unlike nushell, Common Lisp has O(1) mutable arrays and hash tables, so the
awkward rewrites nushell needed are absent. What is left is mostly places where
the Python was shaped by numba.

- **Day 3b** — Python scans for `do()`/`don't()` byte offsets and builds active
  ranges. Lisp makes one pass with an on/off flag. Same partition of the string.
- **Day 7b** — Python undoes a concatenation with string suffix tests. Lisp does
  it with `mod` and `floor` against the matching power of ten. Same test.
- **Day 8** — Python rescans the whole grid once per character class (`'0'`
  through `'z'`), an artifact of writing for numba. Lisp groups antenna
  positions by frequency in one pass. Same pairs.
- **Day 10a** — Python collects `(start, end)` pairs in one global set. Lisp
  marks the reachable 9s in a bit vector per trailhead and counts them. Same
  total.
- **Day 10, both parts** — Python threads a `visited` grid through the DFS.
  Heights rise by exactly 1 per step, so a trail can never revisit a cell and
  the check never fires; Lisp omits it. Dead code in the Python too.
- **Day 9b** — Python pops an exactly-filled gap out of its list. Lisp leaves it
  in place at length 0, which no file fits. Same result, nothing shifts.
- **Day 6** — Python steps into walls and backs out; Lisp looks at the next cell
  before moving. Same path. Part b keeps the Python's `(cell, direction)` bit
  array, allocated once and cleared per candidate.

## What the type declarations are worth

SBCL compiles to native code either way, but the arithmetic it emits depends on
what it can prove about the operand ranges. `fixnum + fixnum` can leave fixnum
range, so a `fixnum` declaration is not enough on its own: the compiler falls
back to a generic call. `compile-file` says so, and the notes name the function.

Two of these mattered here:

| Change | Before | After |
|---|---|---|
| Day 6b: row/column indices from `fixnum` to `(integer -1 4096)` | 118 ms | 66 ms |
| Day 4a: grid indices to `(unsigned-byte 16)`, deltas to `(integer -1 1)` | 1.73 ms | 1.15 ms |

Day 6b packs `(row, column, direction)` into one index, so the bound on a
coordinate decides whether `(* i n)` is a shift-and-add or a call into the
bignum path. Bounding it is one `deftype` and roughly halves the day.

Narrowing is not free, though. Moving day 9's position and length arrays from
`fixnum` to `(signed-byte 32)` made part b **slower**, 16 ms to 23 ms: the
elements have to be re-tagged on every read, and the arithmetic over them was
already inline.

## Results

Compute only, best of 3, in milliseconds. The nushell column is from the earlier
session recorded in `notes/nushell.md`; its Python numbers match the ones here to
within a few percent, so the three sit on the same scale.

| Part | Python impl | Python | Lisp | Lisp / Python | nushell |
|---|---|---|---|---|---|
| 1a | numpy | 0.38 | 0.55 | 1.45x | 4.34 |
| 1b | numpy | 0.39 | 0.12 | 0.32x | 17.6 |
| 2a | numpy per line | 9.72 | 0.30 | 0.03x | 262 |
| 2b | numpy per line | 29.64 | 0.32 | 0.01x | 791 |
| 3a | regex + numpy | 0.27 | 0.23 | 0.87x | 3.42 |
| 3b | regex + numpy | 0.19 | 0.63 | 3.25x | 2.28 |
| 4a | plain loops | 86.84 | 1.15 | 0.01x | 992 |
| 4b | plain loops | 17.53 | 0.27 | 0.02x | 77.6 |
| 5a | numpy bool matrix | 1.48 | 0.38 | 0.25x | 108 |
| 5b | numpy bool matrix | 2.66 | 0.41 | 0.15x | 225 |
| 6a | numba | 0.63 | 0.20 | 0.32x | 69.4 |
| 6b | numba | 46.84 | 66.69 | 1.42x | - |
| 7a | plain recursion | 3.51 | 0.49 | 0.14x | - |
| 7b | plain recursion | 7.27 | 0.70 | 0.10x | - |
| 8a | numba | 0.20 | 0.04 | 0.20x | - |
| 8b | numba | 0.21 | 0.04 | 0.17x | - |
| 9a | numba | 2.08 | 1.88 | 0.90x | - |
| 9b | numba | 8.12 | 16.52 | 2.04x | - |
| 10a | plain recursion | 8.49 | 0.20 | 0.02x | - |
| 10b | numba | 0.37 | 0.17 | 0.45x | - |

Totals: **Python 227 ms, Lisp 91 ms.**

## Reading the spread

Lisp wins 16 of the 20 parts, and the four it loses are the ones that say the
most.

- **Where Python stays in the interpreter, it is not close.** Days 2, 4a, 7 and
  10a are plain loops and recursion on both sides, and Lisp runs them 7x to 70x
  faster. Day 4a is the extreme: the Python indexes a numpy array one scalar at
  a time, which is slower than a list of lists would have been.
- **Where Python reaches numpy on whole arrays, the gap closes.** Days 1, 3 and
  5 land within a small factor either way. Day 3b is Lisp's worst part, 3.25x,
  and it is the one place a real regex engine would have helped: Python runs
  `re.findall` over the input in C while the Lisp walks it character by
  character.
- **Where Python reaches numba, it wins outright.** 6b and 9b are the only two
  parts where compiled Python beats compiled Lisp, by 1.4x and 2x. Both are
  tight scalar loops over a preallocated array, which is exactly what LLVM is
  good at and where SBCL's fixed register allocation and safety checks cost
  something. 2x against LLVM for the same algorithm, written plainly, is a fair
  price.

So the honest summary is that SBCL sits near numba and well above CPython, and
the places it gives ground are narrow and identifiable. Compare that with
nushell, which trails Python by 4x to 112x and has no in-process escape hatch at
all.

## Startup

Compute time is only part of the story for a puzzle runner.

| | Wall clock |
|---|---|
| `sbcl --script /dev/null` | 3 ms |
| `sbcl --script run.lisp`, fasls cached, all 20 parts | 118 ms |
| `sbcl --script run.lisp`, cold, compiling all 11 files | 244 ms |
| Python, cold process, importing the 10 modules and solving all 20 parts | 1450 ms |

Python's 1.45 s is almost all `import numpy` and `import numba`. The Lisp
compiles from source in a quarter of a second and, once `.cache/` holds the
fasls, is running solutions 20 ms after the process starts.

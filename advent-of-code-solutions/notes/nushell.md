# Nushell vs Python on AoC 2024, days 1-10

> **Layout note.** These measurements were taken with the earlier in-process runner (all solutions
> loaded into one process, compiled files cached). The solutions have since become standalone
> scripts, `solutions/2024/dNN.{ext}`, each started in its own process with `just lang=... run`, so
> startup and compile time now show up per run. The algorithm comparisons still hold; the
> `run.lisp` and `just test` commands mentioned below no longer exist (`just check 2024` replaces them).

The nushell solutions in `solutions/2024/d*.nu` transliterate the Python in
`python/src/advent/advent2024/`. The point was to run identical algorithms in
both languages and see where nushell lands.

## Method

- Inputs are the real puzzle inputs, cached in `inputs/2024/` (copied from the Rust cache).
- Both sides are measured **compute only**, with the interpreter already up and
  the input already read. Python gets a warm-up call first so numba's JIT and
  its on-disk cache are not counted; nushell has no warm-up to give it.
- Fast parts report the best of 3 runs, parts over 2s a single run.
- Every nushell answer was checked against the Python answer on the real input,
  and against the puzzle example in each module's `test_string`.

## The comparison is not apples to apples

Six of the ten Python solutions are numpy or plain Python. **Four are numba:
days 6, 8, 9 and 10 run `@njit` native code**, so those rows compare a nushell
interpreter against compiled machine code, not against Python.

## Where the transliteration deviates

Kept faithful everywhere the languages allowed. The exceptions:

- **Day 3b** — Python scans for `do()`/`don't()` byte offsets and builds active
  ranges. Nushell has no "find all offsets", so it splits on `don't()` and keeps
  the text after each `do()`. Same partition of the string.
- **Day 8** — Python rescans the whole grid once per character class (`'0'`
  through `'z'`), an artifact of writing for numba. Nushell groups antenna
  positions by frequency in one pass. Same pairs.
- **Day 9a** — Python mutates a 95k-element disk array with two pointers.
  Nushell has no O(1) mutable array, so it pairs the gaps in the filled prefix
  against the blocks past it, which is what the two pointers converge to.
- **Day 10** — Python threads a `visited` grid through the DFS. Heights rise by
  exactly 1 per step, so a trail can never revisit a cell and the check never
  fires; nushell omits it. Dead code in the Python too.
- **Day 6b** — Python records `(cell, direction)` states in an `(m, n, 4)`
  array to detect a loop. Nushell has no structure that can do that without
  copying, so it uses a step budget instead: more steps than there are states
  means a loop. Same answer, far more steps.
- **Day 4** — the grid is flattened to one list so a cell costs one `get`
  instead of two, and the bounds check tests the far endpoint rather than
  looping over all four offsets. Equivalent, since the intermediate cells of a
  straight run are bounded by its ends.

## Why nushell has no mutable grid

Measured directly, on 10k-element structures:

| Operation | Cost |
|---|---|
| `update` one index of a 10k list | ~225 us (copies the list) |
| build a 1k-key record by `upsert` | 19.5 ms |
| build a 10k-key record by `upsert` | 1.66 s (85x for 10x the keys) |
| 1k lookups in a 1k record | 2.0 ms (2 us each) |
| 1k lookups in a 10k record | 10.4 ms (10 us each) |

Records are scanned linearly, not hashed, so insert and lookup are both O(n),
and building one is O(n^2). Lists are copied on update. `mut` does not change
this: reassigning a `mut` list costs the same as folding it. So nushell has no
O(1) mutable map or array at all, which is what makes days 6 and 9 awkward
rather than merely slow.

## Results

Compute only, interpreter warm, best of 3. Ratio is nushell / Python.

| Part | Python impl | Python | nushell | ratio |
|---|---|---|---|---|
| 1a | numpy | 0.36 ms | 4.34 ms | 12x |
| 1b | numpy | 0.42 ms | 17.6 ms | 42x |
| 2a | numpy per line | 9.40 ms | 262 ms | 28x |
| 2b | numpy per line | 29.2 ms | 791 ms | 27x |
| 3a | regex + numpy | 0.27 ms | 3.42 ms | 13x |
| 3b | regex + numpy | 0.20 ms | 2.28 ms | 12x |
| 4a | plain loops | 86.3 ms | 992 ms | 12x |
| 4b | plain loops | 17.4 ms | 77.6 ms | 4x |
| 5a | numpy bool matrix | 1.48 ms | 108 ms | 73x |
| 5b | numpy bool matrix | 2.60 ms | 225 ms | 87x |
| 6a | numba | 0.62 ms | 69.4 ms | 112x |
| 6b | numba | 45.6 ms | not measured | - |
| 7a-10b | see above | 0.19-8.5 ms | not measured | - |

Days 7 through 10 were implemented and verified but not benchmarked; the run was
stopped during 6b, which was still going after several minutes. Day 6b is the
worst case for nushell by construction: lacking a set to record
`(cell, direction)` states, it burns the full step budget on every one of the
1304 looping obstacles.

All nushell answers matched Python on the real inputs for every part that ran,
and all 20 parts matched the puzzle examples.

## Reading the spread

The ratio swings from 4x to 112x, and it tracks one thing: whether the Python
stayed in the interpreter.

- Day 4 is plain nested loops over a grid on both sides. Nushell is 4-12x
  slower. (Python is unusually slow here too - it indexes a numpy array one
  scalar at a time, which is worse than a list of lists - so this flatters
  nushell somewhat.)
- Days 5 and 6 are where Python reaches an O(1) numpy bool matrix or numba
  native code. Nushell, with a linearly-scanned record standing in for the
  matrix, falls 73-112x behind.

So the interpreter itself is within roughly an order of magnitude of CPython.
The large gaps come from Python's escape hatches into native code and O(1)
containers, which nushell has no in-process equivalent for. Its escape hatch is
the plugin protocol, and a plugin lives in another process: `nu_plugin_polars`
costs about 26 ms to spawn, which only amortises in a long-lived session.

## Known slow case

`solutions/2024/d06.nu` part b does not finish in 60 seconds, so the file carries an `aoc: skip` marker and
`just check` leaves it out unless you set `all=1`. Every other Nushell day matches the Python answers.

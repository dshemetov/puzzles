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

## Rust Usage

In the `rust` directory, run the following commands.

```sh
# Compile and run all solutions.
cargo run --release
```

## Stats

### 2024 Julia Runtimes

Managed to get Julia to run in under 1 second for all 2024 problems.

```
50×7 DataFrame
 Row │ year   day    part  value                              time       kilobytes       gctime
     │ Int64  Int64  Char  Any                                Float64    Float64         Float64
─────┼─────────────────────────────────────────────────────────────────────────────────────────────
   1 │  2024      1  a     1834060                            0.001497    91499.5        0.0810007
   2 │  2024      1  b     21607792                           0.0006266   12002.3        0.0
   3 │  2024      2  a     670                                0.0013363   31280.2        0.0439118
   4 │  2024      2  b     700                                0.0006897       1.511e5    0.0497184
   5 │  2024      3  a     159892596                          0.0003821   81038.7        0.157507
   6 │  2024      3  b     92626942                           0.0011151   67194.9        0.0155559
   7 │  2024      4  a     2336                               0.0014092   18111.9        0.0
   8 │  2024      4  b     2630                               0.0003395    4033.6        0.0
   9 │  2024      5  a     6505                               0.0006594   10845.9        0.0
  10 │  2024      5  b     6897                               0.0005755   15675.4        0.0
  11 │  2024      6  a     4789                               0.001057    30397.9        0.0127697
  12 │  2024      6  b     1304                               0.0402703   12185.6        0.0
  13 │  2024      7  a     2314935962622                      0.0018081   11949.3        0.0
  14 │  2024      7  b     401477450831495                    0.0032546   12134.5        0.0
  15 │  2024      8  a     273                                0.0005449   46693.0        0.0124892
  16 │  2024      8  b     1017                               0.0004113    5007.75       0.0
  17 │  2024      9  a     6201130364722                      0.0006259   26859.5        0.0
  18 │  2024      9  b     6221662795602                      0.0035988   17542.1        0.0153219
  19 │  2024     10  a     611                                0.0010782   34756.7        0.0
  20 │  2024     10  b     1380                               0.0009342   15176.2        0.0
  21 │  2024     11  a     217443                             0.0004354   23989.8        0.0172833
  22 │  2024     11  b     257246536026785                    0.010977    25634.1        0.0
  23 │  2024     12  a     1371306                            0.0294291   38619.5        0.0126956
  24 │  2024     12  b     805880                             0.029991    26346.1        0.0
  25 │  2024     13  a     29201                              0.0031515       2.15818e5  0.0420473
  26 │  2024     13  b     104140871044942                    0.0054319       2.4124e5   0.0589062
  27 │  2024     14  a     228690000                          0.0016194   63462.1        0.0166024
  28 │  2024     14  b     7093                               0.108669        2.7672e5   0.0467607
  29 │  2024     15  a     1421727                            0.0436543   98087.5        0.0138227
  30 │  2024     15  b     1463160                            0.0503082       1.20565e5  0.0300379
  31 │  2024     16  a     66404                              0.0091975   50431.3        0.0
  32 │  2024     16  b     433                                0.0142132   48466.6        0.0180512
  33 │  2024     17  a     7,4,2,5,1,4,6,0,4                  0.0001413   11415.9        0.0
  34 │  2024     17  b     164278764924605                    0.0001263    8601.65       0.0
  35 │  2024     18  a     438                                0.0023717   43229.0        0.0
  36 │  2024     18  b     26,22                              0.0217959   12516.6        0.0
  37 │  2024     19  a     319                                0.0463919   87710.9        0.0155975
  38 │  2024     19  b     692575723305545                    0.0633111   17867.1        0.0
  39 │  2024     20  a     1367                               0.0147713   39640.1        0.0
  40 │  2024     20  b     1006850                            0.0146032    3184.89       0.0
  41 │  2024     21  a     182844                             0.0005948       1.06649e5  0.0181121
  42 │  2024     21  b     226179529377982                    0.0003725    8270.88       0.0
  43 │  2024     22  a     16894083306                        0.0069617     914.195      0.0
  44 │  2024     22  b     1925                               0.0567392       1.5328e5   0.0349826
  45 │  2024     23  a     1156                               0.0255366   41112.4        0.0
  46 │  2024     23  b     ('b', 'x')-('c', 'x')-('d', 'r')…  0.01076     19172.9        0.0
  47 │  2024     24  a     63168299811048                     0.0007665  110598.0        0.0349043
  48 │  2024     24  b     dwp,ffj,gjh,jdr,kfm,z08,z22,z31    3.47e-5       732.031      0.0
  49 │  2024     25  a     2900                               0.0034542   32613.3        0.135733
  50 │  2024     25  b     0                                  3.48e-5        89.8906     0.0

Total time: 0.63806 seconds
```

### 2024 Python Runtimes

Sub 1s Python too! Numba!

```
                                              2024 Solutions
┏━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Day ┃ Part ┃                                                     Answer ┃ Time Taken ┃ Prev Time Taken ┃
┡━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ 1   │ a    │                                                    1834060 │    0.00078 │         0.00142 │
│ 1   │ b    │                                                   21607792 │    0.00053 │         0.00055 │
│ 2   │ a    │                                                        670 │    0.00684 │         0.00714 │
│ 2   │ b    │                                                        700 │    0.02007 │         0.02018 │
│ 3   │ a    │                                                  159892596 │    0.00038 │         0.00115 │
│ 3   │ b    │                                                   92626942 │    0.00027 │         0.00032 │
│ 4   │ a    │                                                       2336 │    0.05826 │         0.05511 │
│ 4   │ b    │                                                       1831 │    0.01436 │         0.01385 │
│ 5   │ a    │                                                       6505 │    0.00157 │         0.00200 │
│ 5   │ b    │                                                       6897 │    0.00203 │         0.00202 │
│ 6   │ a    │                                                       4789 │    0.00151 │         0.00197 │
│ 6   │ b    │                                                       1304 │    0.03899 │         0.03774 │
│ 7   │ a    │                                              2314935962622 │    0.00282 │         0.00312 │
│ 7   │ b    │                                            401477450831495 │    0.00585 │         0.00610 │
│ 8   │ a    │                                                        273 │    0.00035 │         0.00077 │
│ 8   │ b    │                                                       1017 │    0.00026 │         0.00028 │
│ 9   │ a    │                                              6201130364722 │    0.00215 │         0.00292 │
│ 9   │ b    │                                              6221662795602 │    0.00826 │         0.00810 │
│ 10  │ a    │                                                        611 │    0.00618 │         0.00643 │
│ 10  │ b    │                                                       1380 │    0.00036 │         0.00038 │
│ 11  │ a    │                                                     217443 │    0.00047 │         0.00105 │
│ 11  │ b    │                                            257246536026785 │    0.01317 │         0.01226 │
│ 12  │ a    │                                                    1371306 │    0.00925 │         0.00962 │
│ 12  │ b    │                                                     805880 │    0.03864 │         0.03850 │
│ 13  │ a    │                                                      29201 │    0.00066 │         0.00124 │
│ 13  │ b    │                                            104140871044942 │    0.00070 │         0.00082 │
│ 14  │ a    │                                                  228690000 │    0.00087 │         0.00143 │
│ 14  │ b    │                                                       7093 │    0.01690 │         0.01657 │
│ 15  │ a    │                                                    1421727 │    0.06270 │         0.05952 │
│ 15  │ b    │                                                    1463160 │    0.05205 │         0.03168 │
│ 16  │ a    │                                                      66404 │    0.05504 │         0.01503 │
│ 16  │ b    │                                                        433 │    0.03721 │         0.04756 │
│ 17  │ a    │                                          7,4,2,5,1,4,6,0,4 │    0.00017 │         0.00054 │
│ 17  │ b    │                                            164278764924605 │    0.00023 │         0.00027 │
│ 18  │ a    │                                                        438 │    0.00252 │         0.00327 │
│ 18  │ b    │                                                      26,22 │    0.06739 │         0.07036 │
│ 19  │ a    │                                                        319 │    0.05878 │         0.05961 │
│ 19  │ b    │                                            692575723305545 │    0.00825 │         0.00787 │
│ 20  │ a    │                                                       1367 │    0.03850 │         0.03821 │
│ 20  │ b    │                                                    1006850 │    0.03771 │         0.03764 │
│ 21  │ a    │                                                     182844 │    0.00018 │         0.00055 │
│ 21  │ b    │                                            226179529377982 │    0.00054 │         0.00053 │
│ 22  │ a    │                                                16894083306 │    0.00736 │         0.00822 │
│ 22  │ b    │                                                       1925 │    0.06810 │         0.06439 │
│ 23  │ a    │                                                       1156 │    0.03348 │         0.03316 │
│ 23  │ b    │          ('b', 'x')-('c', 'x')-('d', 'r')-('d', 'x')-('i', │    0.03595 │         0.05908 │
│     │      │     's')-('j', 'g')-('k', 'm')-('k', 't')-('l', 'i')-('l', │            │                 │
│     │      │                      't')-('n', 'h')-('u', 'f')-('u', 'm') │            │                 │
│ 24  │ a    │                                             63168299811048 │    0.00108 │         0.00062 │
│ 24  │ b    │                            dwp,ffj,gjh,jdr,kfm,z08,z22,z31 │    0.00009 │         0.00010 │
│ 25  │ a    │                                                       2900 │    0.02494 │         0.02594 │
│ 25  │ b    │                                                          0 │    0.00010 │         0.00010 │
└─────┴──────┴────────────────────────────────────────────────────────────┴────────────┴─────────────────┘
                                         Total time taken: 0.845.
```

## Background

I first got into Advent of Code over the 2015 Christmas holiday with my friend Evin at his family home in LA.
After a few days of only playing SSX Tricky and drinking peppermint schnapps, we were ready to re-engage our brains.
Evin got functional with JavaScript and I was just getting started with Python.
Doing puzzles while cozy with friends is one of my favorite things to do.

- AoC 2024: 50/50 Python (Numba), 50/50 Julia.
- AoC 2023: 32/50 Python, 2/50 Rust.
- AoC 2022: 24/50 Python.
- AoC 2021: 47/50 Python.
- AoC 2020: 32/50 Python.
- AoC 2019: 16/50 Python, ??/50 Mathematica.
- AoC 2018: 25/50 Mathematica. Lessons learned:
  - Mathematica pros: great builtins, great documentation, great plotting, great mathematical notation support.
  - Mathematica cons: [no lazy iteration](https://mathematica.stackexchange.com/questions/226334/breaking-functional-loops-and-doing-lazy-evaluation-in-mathematica), I don't enjoy debugging or building custom data structures in it, notebooks don't render well outside the closed ecosystem.
- AoC 2015: 14/50 Python.

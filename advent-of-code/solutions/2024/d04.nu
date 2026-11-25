# 4. https://adventofcode.com/2024/day/4

# The grid is flattened so a cell costs one `get` instead of two.
def load []: string -> record<flat: list<string>, m: int, n: int> {
    let rows = $in | str trim | lines
    {flat: ($rows | each {|r| $r | split chars } | flatten), m: ($rows | length), n: ($rows | first | str length)}
}

export def a []: string -> int {
    let g = load
    let flat = $g.flat
    let m = $g.m
    let n = $g.n
    mut total = 0
    for i in 0..<$m {
        for j in 0..<$n {
            for d in [[0 1] [1 0] [1 1] [-1 1]] {
                for sgn in [1 -1] {
                    let dx = $sgn * $d.0
                    let dy = $sgn * $d.1
                    let x = $i + 3 * $dx
                    let y = $j + 3 * $dy
                    if $x < 0 or $x >= $m or $y < 0 or $y >= $n { continue }
                    if (($flat | get ($i * $n + $j)) == "X"
                        and ($flat | get (($i + $dx) * $n + $j + $dy)) == "M"
                        and ($flat | get (($i + 2 * $dx) * $n + $j + 2 * $dy)) == "A"
                        and ($flat | get ($x * $n + $y)) == "S") {
                        $total += 1
                    }
                }
            }
        }
    }
    $total
}

export def b []: string -> int {
    let g = load
    let flat = $g.flat
    let m = $g.m
    let n = $g.n
    mut total = 0
    for i in 1..($m - 2) {
        for j in 1..($n - 2) {
            if ($flat | get ($i * $n + $j)) != "A" { continue }
            let ur = $flat | get (($i - 1) * $n + $j + 1)
            let dl = $flat | get (($i + 1) * $n + $j - 1)
            let ul = $flat | get (($i - 1) * $n + $j - 1)
            let dr = $flat | get (($i + 1) * $n + $j + 1)
            let upright = ($ur == "M" and $dl == "S") or ($ur == "S" and $dl == "M")
            let downright = ($ul == "M" and $dr == "S") or ($ul == "S" and $dr == "M")
            if $upright and $downright { $total += 1 }
        }
    }
    $total
}

export const test_string = "
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"

def report [name: string, run: closure] {
    let start = date now
    print (do $run)
    print --stderr $"($name): ((date now) - $start | format duration sec)"
}

export def main [input: path] {
    let s = open --raw $input
    report "part_a" { $s | a }
    report "part_b" { $s | b }
}

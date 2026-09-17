# 6. https://adventofcode.com/2024/day/6

const DIRECTIONS = [[-1 0] [0 1] [1 0] [0 -1]]
const TURN_RIGHT = [1 2 3 0]

def load []: string -> record {
    let rows = $in | str trim | lines
    let m = $rows | length
    let n = $rows | first | str length
    let flat = $rows | each {|r| $r | split chars } | flatten
    let start = $flat | enumerate | where item == "^" | first | get index
    {flat: ($flat | each {|c| if $c == "^" { "." } else { $c } }), m: $m, n: $n, start: $start}
}

export def a []: string -> int {
    let g = load
    let start_i = $g.start // $g.n
    let start_j = $g.start mod $g.n
    generate {|st|
        if $st.i < 0 or $st.i >= $g.m or $st.j < 0 or $st.j >= $g.n { return {} }
        let d = $DIRECTIONS | get $st.d
        if ($g.flat | get ($st.i * $g.n + $st.j)) == "#" {
            {next: {i: ($st.i - $d.0), j: ($st.j - $d.1), d: ($TURN_RIGHT | get $st.d)}}
        } else {
            {out: ($st.i * $g.n + $st.j), next: {i: ($st.i + $d.0), j: ($st.j + $d.1), d: $st.d}}
        }
    } {i: $start_i, j: $start_j, d: 0}
    | uniq
    | length
}

# A walk that revisits a (cell, direction) pair is looping. Without an O(1) set
# to record those pairs, the step budget stands in: more steps than there are
# states means a loop.
def loops [g: record, obstacle: int, start_i: int, start_j: int]: nothing -> bool {
    let budget = $g.m * $g.n * 4
    mut i = $start_i
    mut j = $start_j
    mut d = 0
    mut steps = 0
    mut looping = false
    loop {
        if $i < 0 or $i >= $g.m or $j < 0 or $j >= $g.n { break }
        if $steps > $budget { $looping = true; break }
        $steps += 1
        let dir = $DIRECTIONS | get $d
        let ni = $i + $dir.0
        let nj = $j + $dir.1
        let blocked = if $ni < 0 or $ni >= $g.m or $nj < 0 or $nj >= $g.n {
            false
        } else {
            ($ni * $g.n + $nj) == $obstacle or ($g.flat | get ($ni * $g.n + $nj)) == "#"
        }
        if $blocked { $d = ($TURN_RIGHT | get $d) } else { $i = $ni; $j = $nj }
    }
    $looping
}

export def b []: string -> int {
    let g = load
    let start_i = $g.start // $g.n
    let start_j = $g.start mod $g.n
    let path = generate {|st|
        if $st.i < 0 or $st.i >= $g.m or $st.j < 0 or $st.j >= $g.n { return {} }
        let d = $DIRECTIONS | get $st.d
        if ($g.flat | get ($st.i * $g.n + $st.j)) == "#" {
            {next: {i: ($st.i - $d.0), j: ($st.j - $d.1), d: ($TURN_RIGHT | get $st.d)}}
        } else {
            {out: ($st.i * $g.n + $st.j), next: {i: ($st.i + $d.0), j: ($st.j + $d.1), d: $st.d}}
        }
    } {i: $start_i, j: $start_j, d: 0} | uniq | where {|p| $p != $g.start }

    $path | where {|p| loops $g $p $start_i $start_j } | length
}

export const test_string = "
....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...
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

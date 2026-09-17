# 10. https://adventofcode.com/2024/day/10

const STEPS = [[0 1] [0 -1] [1 0] [-1 0]]

def load []: string -> record {
    let rows = $in | str trim | lines
    {flat: ($rows | each {|r| $r | split chars | into int } | flatten), m: ($rows | length), n: ($rows | first | str length)}
}

# Heights rise by exactly 1 each step, so a trail cannot revisit a cell and the
# visited set the Python carries is never consulted.
def trails [g: record, pos: int]: nothing -> list<int> {
    let height = $g.flat | get $pos
    if $height == 9 { return [$pos] }
    let i = $pos // $g.n
    let j = $pos mod $g.n
    $STEPS | each {|s|
        let ni = $i + $s.0
        let nj = $j + $s.1
        if $ni < 0 or $ni >= $g.m or $nj < 0 or $nj >= $g.n {
            []
        } else {
            let np = $ni * $g.n + $nj
            if (($g.flat | get $np) - $height) != 1 { [] } else { trails $g $np }
        }
    } | flatten
}

def trailheads [g: record]: nothing -> list<int> {
    $g.flat | enumerate | where item == 0 | get index
}

export def a []: string -> int {
    let g = load
    trailheads $g | each {|start| trails $g $start | uniq | length } | math sum
}

export def b []: string -> int {
    let g = load
    trailheads $g | each {|start| trails $g $start | length } | math sum
}

export const test_string = "
89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732
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

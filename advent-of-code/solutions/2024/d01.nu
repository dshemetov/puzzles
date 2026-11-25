# 1. https://adventofcode.com/2024/day/1

export def parse-lists []: string -> record<left: list<int>, right: list<int>> {
    let t = $in | str trim | lines | split column --regex '\s+' left right | into int left right
    {left: $t.left, right: $t.right}
}

export def a []: string -> int {
    let d = parse-lists
    ($d.left | sort) | zip ($d.right | sort) | each {|p| ($p.0 - $p.1) | math abs } | math sum
}

export def b []: string -> int {
    let d = parse-lists
    let counts = $d.right | uniq --count
        | reduce --fold {} {|r, acc| $acc | insert ($r.value | into string) $r.count }
    $d.left | each {|v| $v * ($counts | get --optional ($v | into string) | default 0) } | math sum
}

export const test_string = "
3   4
4   3
2   5
1   3
3   9
3   3
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

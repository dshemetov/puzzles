# 2. https://adventofcode.com/2024/day/2

export def parse-reports []: string -> list<list<int>> {
    str trim | lines | each {|l| $l | split row --regex '\s+' | into int }
}

# Safe when the steps all go one way and each is 1, 2 or 3 apart.
export def is-safe [nums: list<int>]: nothing -> bool {
    let diffs = $nums | window 2 | each {|w| $w.1 - $w.0 }
    let increasing = $diffs | all {|d| $d >= 0 }
    let decreasing = $diffs | all {|d| $d <= 0 }
    let bounded = $diffs | all {|d| $d >= -3 and $d <= 3 and $d != 0 }
    ($increasing or $decreasing) and $bounded
}

export def a []: string -> int {
    parse-reports | where {|r| is-safe $r } | length
}

export def b []: string -> int {
    parse-reports
    | where {|r|
        if (is-safe $r) {
            true
        } else {
            $r | enumerate | any {|it|
                let dropped = $r | drop nth $it.index
                ($dropped | length) >= 2 and (is-safe $dropped)
            }
        }
    }
    | length
}

export const test_string = "
7 6 4 2 1
1 2 7 8 9
9 7 6 2 1
1 3 2 4 5
8 6 4 4 1
1 3 6 7 9
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

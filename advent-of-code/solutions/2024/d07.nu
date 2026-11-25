# 7. https://adventofcode.com/2024/day/7

def parse-equations []: string -> list<list<int>> {
    str trim | lines | each {|l| $l | parse --regex '(\d+)' | get capture0 | into int }
}

# Works backwards from the target, undoing each operator in turn.
export def backtrack [target: int, idx: int, numbers: list<int>, with_combination: bool]: nothing -> bool {
    if $idx == 0 { return ($target == ($numbers | first)) }

    let current = $numbers | get $idx

    if $target > $current and (backtrack ($target - $current) ($idx - 1) $numbers $with_combination) {
        return true
    }

    if ($target mod $current) == 0 and (backtrack ($target // $current) ($idx - 1) $numbers $with_combination) {
        return true
    }

    if $with_combination {
        let num_str = $current | into string
        let target_str = $target | into string
        let keep = ($target_str | str length) - ($num_str | str length)
        if $keep > 0 and ($target_str | str ends-with $num_str) {
            let trimmed = $target_str | str substring 0..<$keep
            if ($trimmed | is-not-empty) and (backtrack ($trimmed | into int) ($idx - 1) $numbers $with_combination) {
                return true
            }
        }
    }

    false
}

def solve [with_combination: bool]: string -> int {
    let totals = parse-equations | each {|line|
        let rest = $line | skip 1
        if (backtrack ($line | first) (($rest | length) - 1) $rest $with_combination) { $line | first } else { 0 }
    }
    [0] ++ $totals | math sum
}

export def a []: string -> int { solve false }
export def b []: string -> int { solve true }

export const test_string = "
190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20
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

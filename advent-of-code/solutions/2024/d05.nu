# 5. https://adventofcode.com/2024/day/5

# Rules become a set of "before_after" keys, standing in for the bit matrix.
def load []: string -> record<rules: record, updates: list<list<int>>> {
    let parts = $in | str trim | split row "\n\n"
    let rules = $parts.0 | lines | reduce --fold {} {|l, acc|
        $acc | upsert ($l | str replace "|" "_") true
    }
    let updates = $parts.1 | lines | each {|l| $l | split row "," | into int }
    {rules: $rules, updates: $updates}
}

def ordered [rules: record, update: list<int>]: nothing -> bool {
    let n = $update | length
    mut ok = true
    for i in 0..<$n {
        for j in ($i + 1)..<$n {
            let key = $"(($update | get $i))_(($update | get $j))"
            if ($rules | get --optional $key | default false) == false {
                $ok = false
                break
            }
        }
        if not $ok { break }
    }
    $ok
}

export def a []: string -> int {
    let d = load
    let valid = $d.updates | where {|u| ordered $d.rules $u }
    let mids = $valid | each {|u| $u | get (($u | length) // 2) }
    [0] ++ $mids | math sum
}

export def b []: string -> int {
    let d = load
    let invalid = $d.updates | where {|u| not (ordered $d.rules $u) }
    let mids = $invalid | each {|update|
        let n = $update | length
        mut u = $update
        for i in 0..<$n {
            for j in ($i + 1)..<$n {
                let key = $"(($u | get $j))_(($u | get $i))"
                if ($d.rules | get --optional $key | default false) {
                    let tmp = $u | get $i
                    $u = ($u | update $i ($u | get $j) | update $j $tmp)
                }
            }
        }
        $u | get ($n // 2)
    }
    [0] ++ $mids | math sum
}

export const test_string = "
47|53
97|13
97|61
97|47
75|29
61|13
75|53
29|13
97|29
53|29
61|53
97|53
61|29
47|13
75|47
97|75
47|61
75|61
47|29
75|13
53|13

75,47,61,53,29
97,61,53,29,13
75,29,13
75,97,47,61,53
61,13,29
97,13,75,29,47
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

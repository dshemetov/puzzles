# 3. https://adventofcode.com/2024/day/3

def mul-sum []: string -> int {
    let products = $in | parse --regex 'mul\((\d+),(\d+)\)'
        | each {|m| ($m.capture0 | into int) * ($m.capture1 | into int) }
    [0] ++ $products | math sum
}

export def a []: string -> int {
    str trim | mul-sum
}

export def b []: string -> int {
    # Everything before the first don't() is live; after one, only the part
    # following the next do() comes back.
    let chunks = $in | str trim | split row "don't()"
    let live = $chunks | skip 1 | each {|c|
        let parts = $c | split row "do()"
        if ($parts | length) > 1 { $parts | skip 1 | str join "do()" } else { "" }
    }
    [($chunks | first)] ++ $live | str join | mul-sum
}

export const test_string = "
xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))
"
export const test_string2 = "
xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))
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

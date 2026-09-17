# 1. https://adventofcode.com/2025/day/1
#
# A 100-position dial starts at 50. Each line turns it right (R) or left (L).
# Part a counts the turns that end on 0, part b counts every pass over 0.

# "R21" -> 21, "L2" -> -2
export def parse-turns []: string -> list<int> {
    lines | each {|turn|
        let magnitude = $turn | str substring 1.. | into int
        if ($turn | str starts-with "R") { $magnitude } else { $magnitude * -1 }
    }
}

export def a []: string -> int {
    parse-turns
    | reduce --fold {pos: 50, count: 0} {|turn, acc|
        let pos = ($acc.pos + $turn) mod 100
        {pos: $pos, count: ($acc.count + (if $pos == 0 { 1 } else { 0 }))}
    }
    | get count
}

export def b []: string -> int {
    parse-turns
    | reduce --fold {pos: 50, count: 0} {|turn, acc|
        let pos = $acc.pos + $turn
        # Position is left unwrapped, so a pass over 0 is a multiple of 100
        # crossed. Landing on one counts, leaving one does not.
        let crossings = if $turn > 0 {
            ($pos // 100) - ($acc.pos // 100)
        } else {
            (($acc.pos - 1) // 100) - (($pos - 1) // 100)
        }
        {pos: $pos, count: ($acc.count + $crossings)}
    }
    | get count
}

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

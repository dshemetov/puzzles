# @URL@

export const example = "
"

export def parse []: string -> list<string> {
    str trim | lines
}

export def a []: string -> int {
    parse
    0
}

export def b []: string -> int {
    parse
    0
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

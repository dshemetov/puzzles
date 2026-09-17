# 8. https://adventofcode.com/2024/day/8

def load []: string -> record {
    let rows = $in | str trim | lines
    let n = $rows | each {|r| $r | str length } | math max
    let padded = $rows | each {|r| $r | fill --alignment l --width $n --character "." }
    {flat: ($padded | each {|r| $r | split chars } | flatten), m: ($rows | length), n: $n}
}

# Antenna positions grouped by frequency, ignoring empty cells.
def antenna-groups [g: record]: nothing -> list<list<int>> {
    $g.flat | enumerate | where item != "." | group-by item | values | each {|rows| $rows | get index }
}

def pairs [ps: list<int>]: nothing -> list<list<int>> {
    $ps | enumerate | each {|x| $ps | skip ($x.index + 1) | each {|y| [$x.item, $y] } } | flatten
}

export def a []: string -> int {
    let g = load
    antenna-groups $g | each {|group|
        pairs $group | each {|p|
            let i1 = $p.0 // $g.n
            let j1 = $p.0 mod $g.n
            let i2 = $p.1 // $g.n
            let j2 = $p.1 mod $g.n
            let di = $i2 - $i1
            let dj = $j2 - $j1
            [[($i2 + $di) ($j2 + $dj)] [($i1 - $di) ($j1 - $dj)]]
        } | flatten
    } | flatten
    | where {|c| $c.0 >= 0 and $c.0 < $g.m and $c.1 >= 0 and $c.1 < $g.n }
    | each {|c| $c.0 * $g.n + $c.1 }
    | uniq | length
}

export def b []: string -> int {
    let g = load
    antenna-groups $g | each {|group|
        pairs $group | each {|p|
            let i1 = $p.0 // $g.n
            let j1 = $p.0 mod $g.n
            let i2 = $p.1 // $g.n
            let j2 = $p.1 mod $g.n
            let di = $i2 - $i1
            let dj = $j2 - $j1
            # Every grid point on the line through the pair, both ways.
            let steps = 0..($g.m + $g.n) | each {|k| $k }
            let forward = $steps | take while {|k|
                let x = $i2 + $k * $di
                let y = $j2 + $k * $dj
                $x >= 0 and $x < $g.m and $y >= 0 and $y < $g.n
            } | each {|k| ($i2 + $k * $di) * $g.n + $j2 + $k * $dj }
            let backward = $steps | take while {|k|
                let x = $i1 - $k * $di
                let y = $j1 - $k * $dj
                $x >= 0 and $x < $g.m and $y >= 0 and $y < $g.n
            } | each {|k| ($i1 - $k * $di) * $g.n + $j1 - $k * $dj }
            $forward ++ $backward
        } | flatten
    } | flatten
    | uniq | length
}

export const test_string = "
............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............
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

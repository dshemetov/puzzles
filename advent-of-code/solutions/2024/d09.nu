# 9. https://adventofcode.com/2024/day/9

# Start offset of every run, since nushell has no cumulative sum.
def run-starts [nums: list<int>]: nothing -> list<int> {
    let count = $nums | length
    generate {|st|
        if $st.i >= $count { return {} }
        {out: $st.pos, next: {i: ($st.i + 1), pos: ($st.pos + ($nums | get $st.i))}}
    } {i: 0, pos: 0}
}

export def a []: string -> int {
    let nums = $in | str trim | split chars | into int
    let disk = $nums | enumerate | each {|x|
        if $x.item == 0 { [] } else if ($x.index mod 2) == 0 {
            1..$x.item | each {|_| $x.index // 2 }
        } else {
            1..$x.item | each {|_| -1 }
        }
    } | flatten

    # Compacting moves every block from beyond the filled prefix into a gap
    # inside it, so the two pointers can be paired off without mutating a disk.
    let filled = $disk | where {|d| $d != -1 } | length
    let head = $disk | first $filled
    let donors = $disk | skip $filled | where {|d| $d != -1 } | reverse

    let kept = $head | enumerate | where item != -1 | each {|x| $x.index * $x.item }
    let gaps = $head | enumerate | where item == -1 | get index
    let moved = $gaps | zip $donors | each {|p| $p.0 * $p.1 }
    [0] ++ $kept ++ $moved | math sum
}

export def b []: string -> int {
    let nums = $in | str trim | split chars | into int
    let starts = run-starts $nums
    let entries = $nums | enumerate | each {|x| {index: $x.index, size: $x.item, pos: ($starts | get $x.index)} }

    let files = $entries | where {|e| ($e.index mod 2) == 0 } | each {|e| {pos: $e.pos, size: $e.size} }
    let gaps = $entries | where {|e| ($e.index mod 2) == 1 and $e.size > 0 }

    mut free_pos = $gaps | each {|e| $e.pos }
    mut free_size = $gaps | each {|e| $e.size }
    mut file_pos = $files | each {|f| $f.pos }
    let file_size = $files | each {|f| $f.size }
    let file_count = $files | length

    for k in 0..<$file_count {
        let file_id = $file_count - 1 - $k
        let size = $file_size | get $file_id
        if $size == 0 { continue }
        let here = $file_pos | get $file_id

        mut slot = -1
        for i in 0..<($free_pos | length) {
            if ($free_pos | get $i) >= $here { break }
            if ($free_size | get $i) >= $size { $slot = $i; break }
        }
        if $slot < 0 { continue }

        $file_pos = ($file_pos | update $file_id ($free_pos | get $slot))
        if ($free_size | get $slot) == $size {
            $free_pos = ($free_pos | drop nth $slot)
            $free_size = ($free_size | drop nth $slot)
        } else {
            $free_pos = ($free_pos | update $slot (($free_pos | get $slot) + $size))
            $free_size = ($free_size | update $slot (($free_size | get $slot) - $size))
        }
    }

    # Each file contributes id * (pos + pos+1 + ... + pos+size-1).
    let final_pos = $file_pos
    let sums = 0..<$file_count | each {|id|
        let size = $file_size | get $id
        let pos = $final_pos | get $id
        $id * ($size * $pos + $size * ($size - 1) // 2)
    }
    [0] ++ $sums | math sum
}

export const test_string = "
2333133121414131402
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

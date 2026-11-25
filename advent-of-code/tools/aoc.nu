# Helpers behind the Justfile recipes. Run from the advent-of-code-solutions root.
# Recipes load this with `use aoc.nu` (the Justfile points NU_LIB_DIRS at tools/).

def pad [day: int]: nothing -> string {
    $day | into string | fill --alignment right --character '0' --width 2
}

export def input-path [day: int, year: int]: nothing -> string {
    $"inputs/($year)/(pad $day).txt"
}

# Download a day's input into inputs/ unless it is already there. Needs AOC_TOKEN.
export def fetch [day: int, year: int] {
    let path = input-path $day $year
    if ($path | path exists) and ((ls $path).0.size > 0b) { return }

    let token = $env.AOC_TOKEN? | default ""
    if $token == "" {
        error make {msg: "set AOC_TOKEN to your adventofcode.com session cookie"}
    }
    let site = $env.AOC_SITE? | default "https://adventofcode.com"
    let response = http get --raw --full --allow-errors --headers {
        User-Agent: "personal-aoc-fetch (nu)"
        Cookie: $"session=($token)"
    } $"($site)/($year)/day/($day)/input"

    if $response.status != 200 {
        error make {
            msg: $"fetch ($year) day ($day) failed \(HTTP ($response.status)\): ($response.body | into string | str substring ..199)"
            help: "A 400 'please log in' means AOC_TOKEN is not a valid session cookie (expired?)."
        }
    }
    mkdir ($path | path dirname)
    $response.body | save --raw --force $path
    print $"saved ($path)"
}

# Create solutions/<year>/dNN.<ext> from the template for that language.
export def new [day: int, ext: string, year: int] {
    let path = $"solutions/($year)/d(pad $day).($ext)"
    if ($path | path exists) { error make {msg: $"($path) already exists"} }
    mkdir ($path | path dirname)
    open --raw $"templates/template.($ext)"
    | str replace --all '@URL@' $"https://adventofcode.com/($year)/day/($day)"
    | save --raw $path
    print $"created ($path)"
}

# The path of a day's solution file, honouring `lang` and `variant`.
export def solution-file [day: int, year: int, lang: string = "", variant: string = ""]: nothing -> string {
    let suffix = if $variant == "" { "" } else { $"-($variant)" }
    let base = $"solutions/($year)/d(pad $day)($suffix)"
    if $lang != "" { return $"($base).($lang)" }

    let found = glob $"($base).*" | sort
    if ($found | is-empty) { error make {msg: $"no solution file ($base).*"} }
    $found | first | path relative-to $env.PWD
}

# The argv that runs a solution file on an input file. The one place to add languages.
export def runner [file: string, input: string]: nothing -> list<string> {
    let p = $file | path parse
    let bin = $".cache/bin/($p.parent | path basename)_($p.stem)"
    match $p.extension {
        py => [uv run $file $input]
        jl => [julia --startup-file=no --project=@aoc $file $input]
        lisp => [sbcl --script $file $input]
        nu => [nu $file $input]
        wl => [wolframscript -file $file $input]
        go => (build $file $bin [go build -o $bin $file] $input)
        rs => (build $file $bin [rustc -O --edition 2024 -o $bin $file] $input)
        _ => (error make {msg: $"no runner for ($file)"})
    }
}

# Compile into .cache/bin when the source is newer, so timing excludes the build.
def build [src: string, bin: string, compile: list<string>, input: string]: nothing -> list<string> {
    mkdir .cache/bin
    let fresh = ($bin | path exists) and ((ls $bin).0.modified > (ls $src).0.modified)
    if not $fresh {
        let r = run-external ($compile | first) ...($compile | skip 1) | complete
        print --stderr $r.stderr
        if $r.exit_code != 0 { error make {msg: $"build of ($src) failed"} }
    }
    [$bin $input]
}

# Run a day (fetching its input if no file is given) and return its output lines.
# `params` are `key=value` strings passed after the input file; a solution reads the ones it declares.
export def answers [day: int, year: int, input: string = "", lang: string = "", variant: string = "", params: list<string> = []]: nothing -> list<string> {
    let input = if $input == "" { fetch $day $year; input-path $day $year } else { $input }
    let argv = runner (solution-file $day $year $lang $variant) $input | append $params
    run-external ($argv | first) ...($argv | skip 1) | lines
}

# Label one answer against answers/<year>.txt: ok / DIFFERS / KNOWN WRONG / unchecked.
export def status [year: int, day: int, part: string, value: string]: nothing -> string {
    let file = $"answers/($year).txt"
    if not ($file | path exists) { return $"  ($part): unchecked" }

    let known = open --raw $file | lines | split column ' ' day part kind value
    | where day == (pad $day) and part == $part
    let right = $known | where kind == right | get value.0?

    if $right == $value { $"  ($part): ok" } else if $right != null {
        $"  ($part): DIFFERS from known right answer ($right)"
    } else if ($known | where kind == wrong and value == $value | is-not-empty) {
        $"  ($part): KNOWN WRONG, do not resubmit"
    } else { $"  ($part): unchecked" }
}

# Print both answers of a day, labelling each on stderr.
export def run-day [day: int, year: int, input: string = "", lang: string = "", variant: string = ""] {
    let out = answers $day $year $input $lang $variant
    for part in (["a" "b"] | enumerate) {
        let value = $out | get -o $part.index | default ""
        print $value
        print --stderr (status $year $day $part.item $value)
    }
}

# Record a day's current answer for a part as right (replacing any earlier right answer) or wrong.
export def record [day: int, year: int, part: string, kind: string, lang: string = "", variant: string = ""] {
    let index = match $part {
        a => 0
        b => 1
        _ => (error make {msg: "part must be a or b"})
    }
    let value = answers $day $year "" $lang $variant | get -o $index | default ""
    if $value == "" { error make {msg: "no answer produced"} }

    let file = $"answers/($year).txt"
    let prefix = $"(pad $day) ($part) ($kind) "
    let kept = if ($file | path exists) { open --raw $file | lines } else { [] }
    | where {|line| if $kind == right { not ($line | str starts-with $prefix) } else { $line != $"($prefix)($value)" } }

    mkdir answers
    $kept | append $"($prefix)($value)" | sort | str join "\n" | $in + "\n" | save --raw --force $file
    print $"recorded: ($prefix)($value)"
}

# A solution file marked `aoc: skip` near the top is left out of batch recipes.
def skipped [file: string]: nothing -> bool {
    open --raw $file | lines | first 8 | any {|line| $line =~ 'aoc: skip' }
}

# Day number and variant parsed from a file name like d09-blocks.py.
def parse-name [file: string]: nothing -> record<day: int, variant: string, ext: string> {
    let m = $file | path basename | parse --regex '^d(?<day>\d+)-?(?<variant>[^.]*)\.(?<ext>.*)$' | first
    {day: ($m.day | into int), variant: $m.variant, ext: $m.ext}
}

def solution-files [year: int, ext: string]: nothing -> list<string> {
    glob $"solutions/($year)/d*.($ext)" | where ($it | path type) == file | sort | path relative-to $env.PWD
}

# Run every solution file in a year and label each answer.
export def check [year: int, timeout: int, ext: string, all: bool] {
    mut skipped = 0
    for file in (solution-files $year $ext) {
        if not $all and (skipped $file) { $skipped += 1; continue }
        let n = parse-name $file
        print ($file | path basename)
        let r = ^timeout $timeout just $"lang=($n.ext)" $"variant=($n.variant)" run $n.day "" $year | complete
        let labels = $r.stderr | lines | where $it =~ '^  [ab]:'
        print ($labels | if ($in | is-empty) { ["  run failed or timed out"] } else { $in } | str join "\n")
    }
    if $skipped > 0 { print $"skipped ($skipped) files marked 'aoc: skip' \(just all=1 check includes them\)" }
}

# The `key=value` lines of an example's .params file, or none.
def example-params [input: string]: nothing -> list<string> {
    let file = $input | str replace --regex '\.txt$' '.params'
    if not ($file | path exists) { return [] }
    open --raw $file | lines | where {|l| $l | str trim | is-not-empty }
}

# Which input and params to use for a day: example `k` (empty for the first, `2` for dNN.2), or "real".
def pick-input [day: int, year: int, k: string]: nothing -> record<input: string, params: list<string>> {
    if $k == "real" { fetch $day $year; return {input: (input-path $day $year), params: []} }
    let suffix = if $k == "" { "" } else { $".($k)" }
    let input = $"examples/($year)/d(pad $day)($suffix).txt"
    if not ($input | path exists) { error make {msg: $"no example ($input)"} }
    {input: $input, params: (example-params $input)}
}

# Run a day on one example (with its params) and show the answers next to the expected ones.
export def example [day: int, year: int, k: string = "", lang: string = "", variant: string = ""] {
    let pick = pick-input $day $year $k
    let expected = $pick.input | str replace --regex '\.txt$' '.expected'
    let want = if ($expected | path exists) { open --raw $expected | lines } else { [] }
    let got = answers $day $year $pick.input $lang $variant $pick.params
    for part in (["a" "b"] | enumerate) {
        let w = $want | get -o $part.index | default ""
        let g = $got | get -o $part.index | default ""
        print $"($part.item): got ($g), expected ($w | if $in == "" { '-' } else { $in })"
    }
}

# Start a Python day under pdb on one example (or `real`). Set breakpoints with `b file:line`, or call `breakpoint()`.
export def debug [day: int, year: int, k: string = "", lang: string = "", variant: string = ""] {
    let file = solution-file $day $year (if $lang == "" { "py" } else { $lang }) $variant
    if ($file | path parse | get extension) != py { error make {msg: "debug supports Python days only (Julia: `just jl-repl`)"} }
    let pick = pick-input $day $year $k
    exec uv run --no-project --with-requirements $file python -m pdb $file $pick.input ...$pick.params
}

# Run a day's tests. Every language runs its normal entry point on each examples/<year>/dNN[.k].txt and
# compares with dNN[.k].expected (one line per part, a then b; a blank line means that part is not checked).
# An optional dNN[.k].params holds `key=value` lines (like `width=11`) passed to the solution after the input file.
# Python also runs doctests (for helper functions) and Rust its `#[test]` functions.
export def test [day: int, year: int, lang: string = "", variant: string = ""] {
    let file = solution-file $day $year $lang $variant
    let ext = $file | path parse | get extension
    mut ran = false
    mut failed = false

    if $ext == py and (open --raw $file | str contains ">>>") {
        $ran = true
        let r = ^uv run --no-project --with-requirements $file python -m doctest -v $file | complete
        print ($r.stdout | lines | last 3 | str join "\n")
        if $r.exit_code != 0 { $failed = true }
    }
    if $ext == rs and (open --raw $file | str contains "#[test]") {
        $ran = true
        mkdir .cache/bin
        let bin = $".cache/bin/test_($file | path parse | get stem)_($year)"
        ^rustc --test -O --edition 2024 -o $bin $file
        let r = ^$bin | complete
        print ($r.stdout | lines | last 3 | str join "\n")
        if $r.exit_code != 0 { $failed = true }
    }

    let stem = $"d(pad $day)"
    let pattern = $"/($stem)" + '(\.[0-9]+)?\.txt$'
    let inputs = try { ls $"examples/($year)" | get name } catch { [] }
    | where {|f| $f =~ $pattern } | sort
    for input in $inputs {
        $ran = true
        let want = open --raw ($input | str replace --regex '\.txt$' '.expected') | lines
        let got = answers $day $year $input $lang $variant (example-params $input)
        let name = $input | path basename
        for part in (["a" "b"] | enumerate) {
            let w = $want | get -o $part.index | default ""
            let g = $got | get -o $part.index | default ""
            if $w == "" { continue }
            if $w == $g { print $"  ($name) ($part.item): ok" } else {
                print $"  ($name) ($part.item): FAILED, expected ($w), got ($g)"
                $failed = true
            }
        }
    }

    if not $ran { error make {msg: $"no tests for ($file) \(no doctests, and no examples/($year)/($stem).txt\)"} }
    if $failed { error make {msg: "tests failed"} }
}

# Time one day with hyperfine (whole process, including interpreter startup).
export def time [day: int, year: int, lang: string = "", variant: string = ""] {
    fetch $day $year
    let argv = runner (solution-file $day $year $lang $variant) (input-path $day $year)
    ^hyperfine -N --warmup 1 ($argv | str join ' ')
}

# Time every day in a year in one hyperfine table.
export def time-year [year: int, all: bool] {
    mut skipped = 0
    mut args = []
    for file in (solution-files $year "*") {
        if not $all and (skipped $file) { $skipped += 1; continue }
        let day = (parse-name $file).day
        fetch $day $year
        $args = $args | append ["-n" ($file | path basename) (runner $file (input-path $day $year) | str join ' ')]
    }
    if $skipped > 0 { print $"skipped ($skipped) files marked 'aoc: skip' \(just all=1 time-year includes them\)" }
    ^hyperfine -N --warmup 1 ...$args
}

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
export def answers [day: int, year: int, input: string = "", lang: string = "", variant: string = ""]: nothing -> list<string> {
    let input = if $input == "" { fetch $day $year; input-path $day $year } else { $input }
    let argv = runner (solution-file $day $year $lang $variant) $input
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

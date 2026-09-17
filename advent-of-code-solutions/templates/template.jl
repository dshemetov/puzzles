# @URL@

const EXAMPLE = """
"""

parse_input(s) = split(strip(s, '\n'), '\n')

part_a(lines) = 0

part_b(lines) = 0

function main(path)
    lines = parse_input(read(path, String))
    for (name, part) in (("part_a", part_a), ("part_b", part_b))
        first_call = @elapsed answer = part(lines)
        println(answer)
        # The first call includes compiling. Call again (if it was quick) to time just the work.
        # A part that mutates `lines` should copy it, or the second call will see changed data.
        warm = first_call < 2 ? @elapsed(part(lines)) : first_call
        println(stderr, name, ": ", round(warm, digits=4), "s (first call ", round(first_call, digits=4), "s)")
    end
end

# Only runs as a script, so `include`-ing this file in a REPL stays quiet.
if abspath(PROGRAM_FILE) == @__FILE__
    main(ARGS[1])
end

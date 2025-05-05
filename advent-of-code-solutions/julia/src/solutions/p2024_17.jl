# My program: 2,4,1,1,7,5,1,5,4,1,5,5,0,3,3,0
# Decompile:
# 2,4 - b = a % 8
# 1,1 - b = b ⊻ 1
# 7,5 - c = a ÷ 2^b
# 1,5 - b = b ⊻ 5
# 4,1 - b = b ⊻ c
# 5,5 - out b % 8
# 0,3 - a = a ÷ 8
# 3,0 - jmp 0 (if A != 0)

# Decompile to words:
# This program processes a number A three bits at a time, from right to left
# For each group of 3 bits:
#   1. Extract last 3 bits into b (b = a % 8)
#   2. Flip the lowest bit of b (b ⊻ 1)
#   3. Use this modified b to right-shift a, storing in c
#   4. Flip bits 1 and 3 of b (b ⊻ 5)
#   5. XOR b with the shifted value from step 3
#   6. Output the last 3 bits of this result
#   7. Remove the processed 3 bits from a (a ÷ 8)

function solve(input::Question{2024,17,'a'})
    if input.s == ""
        s = test_string_2024_17
    else
        s = input.s
    end

    registers = Dict{String,Int}()
    input_integers = [parse(Int, m.match) for m in eachmatch(r"(\d+)", s)]
    registers["A"], registers["B"], registers["C"], program = input_integers[1], input_integers[2], input_integers[3], input_integers[4:end]

    j = 1 # j for Julia (1-indexed)
    out = []
    # println(registers)
    # println(program)
    while j < length(program)
        op, literal, combo = program[j], program[j+1], parse_combo_operand(program[j+1], registers)
        if op == 0 # adv
            registers["A"] = registers["A"] ÷ 2^combo
        elseif op == 1 # bxl (bitwise or)
            registers["B"] = registers["B"] ⊻ literal
        elseif op == 2 # bst
            registers["B"] = combo % 8
        elseif op == 3 && registers["A"] != 0 # jnz
            j = literal + 1 # convert to 1-indexed
            continue
        elseif op == 4 # bxc (bitwise xor)
            registers["B"] = registers["B"] ⊻ registers["C"]
        elseif op == 5 # out
            push!(out, combo % 8)
        elseif op == 6 # bdv
            registers["B"] = registers["A"] ÷ 2^combo
        elseif op == 7 # cdv
            registers["C"] = registers["A"] ÷ 2^combo
        end
        j += 2
    end

    # println(registers)

    # Join out into a string, with commas
    return join(out, ",")
end

function parse_combo_operand(k::Int, registers::Dict{String,Int})
    if 0 <= k <= 3
        return k
    elseif k == 4
        return registers["A"]
    elseif k == 5
        return registers["B"]
    elseif k == 6
        return registers["C"]
    end
end

function solve(input::Question{2024,17,'b'})
    if input.s == ""
        # We don't have a test case for this part
        return 0
    else
        s = input.s
    end

    program = [parse(Int, m.match) for m in eachmatch(r"(\d+)", s)][4:end]
    rev_program = reverse(program)

    valid = []
    function recurse(a, i)
        # println("RECURSE: a = ", a, ", i = ", i, ", length(program) = ", length(program))
        if i > length(program)
            push!(valid, a)
            return a
        end

        # Use the decompiled program to generate valid values of a, three bits
        # at a time
        a2 = a << 3
        for b_ in 0:7
            # Inline the decompiled program, to be extra annoying
            if (b_ ⊻ 4) ⊻ ((a2 + b_) ÷ 2^(b_ ⊻ 1)) % 8 == rev_program[i]
                recurse(a2 + b_, i + 1)
            end
        end
    end

    recurse(0, 1)
    return minimum(valid)
end

test_string_2024_17 = """
Register A: 729
Register B: 0
Register C: 0

Program: 0,1,5,4,3,0
"""

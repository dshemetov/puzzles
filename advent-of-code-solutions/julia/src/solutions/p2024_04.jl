"""4. https://adventofcode.com/2024/day/4"""


function solve(input::Question{2024,4,'a'})
    if input.s == ""
        s = test_string_2024_04
    else
        s = input.s
    end
    s = strip(s, '\n')
    grid = stack([collect(row) for row in split(s, '\n')], dims=1)
    m, n = size(grid)
    total = 0
    word = ['X', 'M', 'A', 'S']
    directions = [(0, 1), (1, 0), (1, 1), (-1, 1)]

    for i in 1:m
        for j in 1:n
            for d in directions
                for sgn in [1, -1]
                    grid_word = [grid[i+sgn*(k-1)*d[1], j+sgn*(k-1)*d[2]] for k in 1:4
                                 if 1 <= i + sgn * (k - 1) * d[1] <= m && 1 <= j + sgn * (k - 1) * d[2] <= n]
                    if grid_word == word
                        total += 1
                    end
                end
            end
        end
    end
    return total
end

function solve(input::Question{2024,4,'b'})
    if input.s == ""
        s = test_string_2024_04
    else
        s = input.s
    end
    s = strip(s, '\n')
    grid = stack([collect(row) for row in split(s, '\n')], dims=1)
    m, n = size(grid)
    total = 0
    word = ['M', 'A', 'S']
    rword = reverse(word)

    for i in 2:m-1
        for j in 2:n-1
            upright = [grid[i-k, j+k] for k in -1:1 if 1 <= i - k <= m && 1 <= j + k <= n]
            downright = [grid[i+k, j+k] for k in -1:1 if 1 <= i + k <= m && 1 <= j + k <= n]
            if (upright == word || upright == rword) && (downright == word || downright == rword)
                total += 1
            end
        end
    end

    return total
end

test_string_2024_04 = """
MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX
"""

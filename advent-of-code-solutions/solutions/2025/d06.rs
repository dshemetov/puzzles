// 2025 day 6: https://adventofcode.com/2025/day/6
#![allow(dead_code)]

/// # Example
/// ```
/// let input = "123 328  51 64\n 45 64  387 23\n  6 98  215 314\n*   +   *   +";
/// assert_eq!(part_a(input.to_string()), "4277556");
/// ```
fn part_a(s: String) -> String {
    let lines: Vec<&str> = s.lines().collect();
    let ops: Vec<&str> = lines.last().unwrap().split_whitespace().collect();
    let num_cols = ops.len();
    let mut cols = vec![Vec::new(); num_cols];
    for line in &lines[..lines.len() - 1] {
        for (i, tok) in line.split_whitespace().enumerate() {
            cols[i].push(tok.parse::<i64>().unwrap());
        }
    }
    cols.iter()
        .zip(ops.iter())
        .map(|(col, &op)| match op {
            "+" => col.iter().sum::<i64>(),
            "*" => col.iter().product::<i64>(),
            _ => panic!("Unknown op: {}", op),
        })
        .sum::<i64>()
        .to_string()
}

/// # Example
/// ```
/// let input = "123 328  51 64\n 45 64  387 23\n  6 98  215 314\n*   +   *   +  ";
/// assert_eq!(part_b(input.to_string()), "3263827");
/// ```
fn part_b(s: String) -> String {
    let lines: Vec<&str> = s.lines().collect();
    let op_line = lines.last().unwrap();
    let data_lines: Vec<&[u8]> = lines[..lines.len() - 1]
        .iter()
        .map(|l| l.as_bytes())
        .collect();
    let width = lines.iter().map(|l| l.len()).max().unwrap();

    // Build vertical strings for each character column
    let col_strings: Vec<String> = (0..width)
        .map(|c| {
            data_lines
                .iter()
                .map(|row| if c < row.len() { row[c] as char } else { ' ' })
                .filter(|ch| ch.is_ascii_digit())
                .collect()
        })
        .collect();

    // Find operations and their column positions
    let ops: Vec<(usize, u8)> = op_line
        .bytes()
        .enumerate()
        .filter(|&(_, b)| b == b'*' || b == b'+')
        .collect();

    // Group columns by operation, parse numbers, apply
    ops.iter()
        .enumerate()
        .map(|(oi, &(start, op))| {
            let end = if oi + 1 < ops.len() {
                ops[oi + 1].0
            } else {
                width
            };
            let numbers: Vec<i64> = col_strings[start..end]
                .iter()
                .filter(|s| !s.is_empty())
                .map(|s| s.parse().unwrap())
                .collect();
            match op {
                b'+' => numbers.iter().sum::<i64>(),
                b'*' => numbers.iter().product::<i64>(),
                _ => unreachable!(),
            }
        })
        .sum::<i64>()
        .to_string()
}

fn main() {
    let path = std::env::args().nth(1).expect("usage: <input file>");
    let input = std::fs::read_to_string(path).expect("could not read input");
    // Trailing newlines are trimmed so every part sees the same text the old runner gave it.
    let input = input.trim().to_string();
    let parts: [(&str, fn(String) -> String); 2] = [("part_a", part_a), ("part_b", part_b)];
    for (name, part) in parts {
        let start = std::time::Instant::now();
        println!("{}", part(input.clone()));
        eprintln!("{}: {:.4}s", name, start.elapsed().as_secs_f64());
    }
}

// 2025 day 12: https://adventofcode.com/2025/day/12
#![allow(dead_code)]

fn parse_input(s: &str) -> (Vec<usize>, Vec<(usize, usize, Vec<usize>)>) {
    let mut shape_sizes: Vec<usize> = Vec::new();
    let mut queries = Vec::new();
    let mut lines = s.lines().peekable();

    while let Some(line) = lines.peek() {
        let line = line.trim();
        if line.is_empty() {
            lines.next();
            continue;
        }
        // Query line: "WxH: n n n ..."
        if line.contains('x') && line.contains(':') {
            if let Some((dims, counts_str)) = line.split_once(':') {
                if let Some((w_str, h_str)) = dims.trim().split_once('x') {
                    if let (Ok(w), Ok(h)) = (w_str.parse::<usize>(), h_str.parse::<usize>()) {
                        let counts: Vec<usize> = counts_str
                            .split_whitespace()
                            .map(|n| n.parse().unwrap())
                            .collect();
                        queries.push((w, h, counts));
                        lines.next();
                        continue;
                    }
                }
            }
        }
        // Shape header: "N:"
        if let Some(idx_str) = line.strip_suffix(':') {
            if idx_str.trim().parse::<usize>().is_ok() {
                lines.next();
                let mut cell_count = 0;
                while let Some(grid_line) = lines.peek() {
                    let grid_line = grid_line.trim();
                    if grid_line.is_empty() || grid_line.contains(':') {
                        break;
                    }
                    cell_count += grid_line.chars().filter(|&ch| ch == '#').count();
                    lines.next();
                }
                shape_sizes.push(cell_count);
                continue;
            }
        }
        lines.next();
    }

    (shape_sizes, queries)
}

fn part_a(s: String) -> String {
    let (shape_sizes, queries) = parse_input(&s);
    queries
        .iter()
        .filter(|(w, h, counts)| {
            let total_cells: usize = counts
                .iter()
                .enumerate()
                .map(|(i, &c)| c * shape_sizes[i])
                .sum();
            total_cells <= w * h
        })
        .count()
        .to_string()
}

fn part_b(_s: String) -> String {
    "0".to_string()
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_area_check() {
        let input = "0:\n#.#\n###\n\n1:\n##\n##\n\n6x3: 2 1\n3x2: 1 1";
        let result = part_a(input.to_string());
        // 2*5 + 1*4 = 14 <= 18 -> true; 1*5 + 1*4 = 9 > 6 -> false. 1 feasible.
        assert_eq!(result, "1");
    }
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

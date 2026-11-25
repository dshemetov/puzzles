// 2025 day 4: https://adventofcode.com/2025/day/4
#![allow(dead_code)]

const DIRS: [(i32, i32); 8] = [
    (-1, -1),
    (-1, 0),
    (-1, 1),
    (0, -1),
    (0, 1),
    (1, -1),
    (1, 0),
    (1, 1),
];

fn count_neighbors(grid: &[u8], cols: usize, rows: usize, idx: usize) -> u8 {
    let r = (idx / cols) as i32;
    let c = (idx % cols) as i32;
    DIRS.iter()
        .filter(|&&(dr, dc)| {
            let nr = r + dr;
            let nc = c + dc;
            nr >= 0
                && nr < rows as i32
                && nc >= 0
                && nc < cols as i32
                && grid[nr as usize * cols + nc as usize] == b'@'
        })
        .count() as u8
}

/// # Example
/// ```
/// let input = "..@@.@@@@.\n@@@.@.@.@@\n@@@@@.@.@@\n@.@@@@..@.\n@@.@@@@.@@\n.@@@@@@@.@\n.@.@.@.@@@\n@.@@@.@@@@\n.@@@@@@@@.\n@.@.@@@.@.";
/// assert_eq!(part_a(input.to_string()), "13");
/// ```
fn part_a(s: String) -> String {
    let rows = s.lines().count();
    let cols = s.lines().next().unwrap().len();
    let grid: Vec<u8> = s.lines().flat_map(|l| l.bytes()).collect();
    (0..grid.len())
        .filter(|&i| grid[i] == b'@' && count_neighbors(&grid, cols, rows, i) < 4)
        .count()
        .to_string()
}

fn part_b(s: String) -> String {
    let rows = s.lines().count();
    let cols = s.lines().next().unwrap().len();
    let mut grid: Vec<u8> = s.lines().flat_map(|l| l.bytes()).collect();
    let mut total = 0;
    loop {
        let to_remove: Vec<usize> = (0..grid.len())
            .filter(|&i| grid[i] == b'@' && count_neighbors(&grid, cols, rows, i) < 4)
            .collect();
        if to_remove.is_empty() {
            break;
        }
        total += to_remove.len();
        for i in to_remove {
            grid[i] = b'.';
        }
    }
    total.to_string()
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

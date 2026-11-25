// 2025 day 7: https://adventofcode.com/2025/day/7
#![allow(dead_code)]

use std::collections::{HashMap, HashSet};

fn find_start(lines: &[&[u8]]) -> (usize, usize) {
    for (r, line) in lines.iter().enumerate() {
        if let Some(c) = line.iter().position(|&b| b == b'S') {
            return (r, c);
        }
    }
    panic!("No start found");
}

fn solve_splits(s: &str) -> usize {
    let lines: Vec<&[u8]> = s.lines().map(|l| l.as_bytes()).collect();
    let (start_row, start_col) = find_start(&lines);
    let mut active: HashSet<usize> = HashSet::new();
    active.insert(start_col);
    let mut total = 0;
    for r in (start_row + 1)..lines.len() {
        let line = lines[r];
        let mut new_active: HashSet<usize> = HashSet::new();
        for c in &active {
            if *c < line.len() && line[*c] == b'^' {
                total += 1;
                if *c > 0 {
                    new_active.insert(c - 1);
                }
                new_active.insert(c + 1);
            } else {
                new_active.insert(*c);
            }
        }
        active = new_active;
    }
    total
}

fn solve_paths(s: &str) -> u64 {
    let lines: Vec<&[u8]> = s.lines().map(|l| l.as_bytes()).collect();
    let (start_row, start_col) = find_start(&lines);
    let mut active: HashMap<usize, u64> = HashMap::new();
    active.insert(start_col, 1);
    for r in (start_row + 1)..lines.len() {
        let line = lines[r];
        let mut new_active: HashMap<usize, u64> = HashMap::new();
        for (&c, &count) in &active {
            if c < line.len() && line[c] == b'^' {
                if c > 0 {
                    *new_active.entry(c - 1).or_default() += count;
                }
                *new_active.entry(c + 1).or_default() += count;
            } else {
                *new_active.entry(c).or_default() += count;
            }
        }
        active = new_active;
    }
    active.values().sum()
}

/// # Example
/// ```
/// let input = ".......S.......\n...............\n.......^.......\n...............\n......^.^......\n...............\n.....^.^.^.....\n...............\n....^.^...^....\n...............\n...^.^...^.^...\n...............\n..^...^.....^..\n...............\n.^.^.^.^.^...^.\n................";
/// assert_eq!(part_a(input.to_string()), "21");
/// ```
fn part_a(s: String) -> String {
    solve_splits(&s).to_string()
}

fn part_b(s: String) -> String {
    solve_paths(&s).to_string()
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

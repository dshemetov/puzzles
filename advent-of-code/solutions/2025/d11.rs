// 2025 day 11: https://adventofcode.com/2025/day/11
#![allow(dead_code)]

use std::collections::HashMap;

fn parse_graph(s: &str) -> HashMap<&str, Vec<&str>> {
    let mut graph = HashMap::new();
    for line in s.lines() {
        let (node, rest) = line.split_once(": ").unwrap();
        let neighbors: Vec<&str> = rest.split_whitespace().collect();
        graph.insert(node, neighbors);
    }
    graph
}

fn count_paths<'a>(
    node: &'a str,
    graph: &HashMap<&'a str, Vec<&'a str>>,
    memo: &mut HashMap<&'a str, u64>,
) -> u64 {
    if node == "out" {
        return 1;
    }
    if let Some(&cached) = memo.get(node) {
        return cached;
    }
    let result = match graph.get(node) {
        Some(neighbors) => neighbors.iter().map(|n| count_paths(n, graph, memo)).sum(),
        None => 0,
    };
    memo.insert(node, result);
    result
}

/// Solve day 11 part A: count all paths from "you" to "out".
///
/// # Example
/// ```
/// let input = "\
/// aaa: you hhh
/// you: bbb ccc
/// bbb: ddd eee
/// ccc: ddd eee fff
/// ddd: ggg
/// eee: out
/// fff: out
/// ggg: out
/// hhh: ccc fff iii
/// iii: out";
/// assert_eq!(part_a(input.to_string()), "5");
/// ```
fn part_a(s: String) -> String {
    let graph = parse_graph(&s);
    let mut memo = HashMap::new();
    count_paths("you", &graph, &mut memo).to_string()
}

fn count_paths_through<'a>(
    node: &'a str,
    visited_mask: u8,
    graph: &HashMap<&'a str, Vec<&'a str>>,
    required: &[&str],
    memo: &mut HashMap<(&'a str, u8), u64>,
) -> u64 {
    let all_required: u8 = (1 << required.len()) - 1;
    if node == "out" {
        return if visited_mask == all_required { 1 } else { 0 };
    }
    if let Some(&cached) = memo.get(&(node, visited_mask)) {
        return cached;
    }
    let result = match graph.get(node) {
        Some(neighbors) => neighbors
            .iter()
            .map(|n| {
                let mut mask = visited_mask;
                if let Some(i) = required.iter().position(|r| r == n) {
                    mask |= 1 << i;
                }
                count_paths_through(n, mask, graph, required, memo)
            })
            .sum(),
        None => 0,
    };
    memo.insert((node, visited_mask), result);
    result
}

/// Solve day 11 part B: count paths from "svr" to "out" passing through both "dac" and "fft".
///
/// # Example
/// ```
/// let input = "\
/// svr: aaa bbb
/// aaa: fft
/// fft: ccc
/// bbb: tty
/// tty: ccc
/// ccc: ddd eee
/// ddd: hub
/// hub: fff
/// eee: dac
/// dac: fff
/// fff: ggg hhh
/// ggg: out
/// hhh: out";
/// assert_eq!(part_b(input.to_string()), "2");
/// ```
fn part_b(s: String) -> String {
    let graph = parse_graph(&s);
    let required = &["dac", "fft"];
    let mut memo = HashMap::new();
    let start_mask = if required.contains(&"svr") { 1u8 } else { 0u8 };
    count_paths_through("svr", start_mask, &graph, required, &mut memo).to_string()
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

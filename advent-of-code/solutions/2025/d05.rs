// 2025 day 5: https://adventofcode.com/2025/day/5
#![allow(dead_code)]

/// # Example
/// ```
/// let input = "3-5\n10-14\n16-20\n12-18\n\n1\n5\n8\n11\n17\n32";
/// assert_eq!(part_a(input.to_string()), "3");
/// ```
fn part_a(s: String) -> String {
    let mut parts = s.split("\n\n");
    let ranges: Vec<(i64, i64)> = parts
        .next()
        .unwrap()
        .lines()
        .map(|l| {
            let mut sp = l.split('-');
            let lo: i64 = sp.next().unwrap().parse().unwrap();
            let hi: i64 = sp.next().unwrap().parse().unwrap();
            (lo, hi)
        })
        .collect();
    parts
        .next()
        .unwrap()
        .lines()
        .filter(|l| {
            let n: i64 = l.parse().unwrap();
            ranges.iter().any(|&(lo, hi)| n >= lo && n <= hi)
        })
        .count()
        .to_string()
}

/// # Example
/// ```
/// let input = "3-5\n10-14\n16-20\n12-18\n\n1\n5\n8\n11\n17\n32";
/// assert_eq!(part_b(input.to_string()), "14");
/// ```
fn part_b(s: String) -> String {
    let ranges_str = s.split("\n\n").next().unwrap();
    let mut ranges: Vec<(i64, i64)> = ranges_str
        .lines()
        .map(|l| {
            let mut sp = l.split('-');
            let lo: i64 = sp.next().unwrap().parse().unwrap();
            let hi: i64 = sp.next().unwrap().parse().unwrap();
            (lo, hi)
        })
        .collect();
    ranges.sort();
    let mut merged: Vec<(i64, i64)> = Vec::new();
    for (lo, hi) in ranges {
        if let Some(last) = merged.last_mut() {
            if lo <= last.1 + 1 {
                last.1 = last.1.max(hi);
                continue;
            }
        }
        merged.push((lo, hi));
    }
    merged
        .iter()
        .map(|(lo, hi)| hi - lo + 1)
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

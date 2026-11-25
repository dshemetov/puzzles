// 2025 day 1: https://adventofcode.com/2025/day/1
#![allow(dead_code)]

fn parse_event(e: &str) -> i32 {
    let (sign, rest) = e.split_at(1);
    let magnitude: i32 = rest.parse().unwrap();
    match sign {
        "R" => magnitude,
        "L" => -magnitude,
        _ => panic!("Invalid direction"),
    }
}

fn part_a(s: String) -> String {
    let (_, count) = s.lines().fold((50, 0), |(val, count), e| {
        let nval = (val + parse_event(e)) % 100;
        (nval, count + if nval == 0 { 1 } else { 0 })
    });
    count.to_string()
}

fn part_b(s: String) -> String {
    let mut val = 50;
    let mut count = 0;
    for e in s.lines() {
        let nval = val + parse_event(e);
        if (val < 0 && nval >= 0) || (val > 0 && nval <= 0) {
            count += 1 + (nval.abs() / 100);
        } else {
            count += nval.abs() / 100;
        }
        val = nval % 100;
    }
    count.to_string()
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

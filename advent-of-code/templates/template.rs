// @URL@
#![allow(unused)]
use std::{env, fs, time::Instant};

const EXAMPLE: &str = "";

fn parse(s: &str) -> Vec<&str> {
    s.trim_matches('\n').lines().collect()
}

fn part_a(lines: &[&str]) -> i64 {
    0
}

fn part_b(lines: &[&str]) -> i64 {
    0
}

fn main() {
    let path = env::args().nth(1).expect("usage: <input file>");
    let raw = fs::read_to_string(path).expect("could not read input");
    let lines = parse(&raw);
    let parts: [(&str, fn(&[&str]) -> i64); 2] = [("part_a", part_a), ("part_b", part_b)];
    for (name, part) in parts {
        let start = Instant::now();
        println!("{}", part(&lines));
        eprintln!("{}: {:.4}s", name, start.elapsed().as_secs_f64());
    }
}

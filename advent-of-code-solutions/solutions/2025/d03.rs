// 2025 day 3: https://adventofcode.com/2025/day/3
#![allow(dead_code)]

/// ```
/// let digits: Vec<u8> = "234234234234278".bytes().map(|b| b - b'0').collect();
/// let expected: Vec<u8> = "434234234278".bytes().map(|b| b - b'0').collect();
/// assert_eq!(day_2025_03::largest_subsequence(&digits, 12), expected);
/// ```
fn largest_subsequence(digits: &[u8], k: usize) -> Vec<u8> {
    let mut stack: Vec<u8> = Vec::with_capacity(k);
    let n = digits.len();
    for (i, &d) in digits.iter().enumerate() {
        let remaining = n - i;
        while stack.len() > 0 && stack.last().unwrap() < &d && stack.len() + remaining > k {
            stack.pop();
        }
        if stack.len() < k {
            stack.push(d);
        }
    }
    stack
}

fn digits_to_number(digits: &[u8]) -> i64 {
    digits.iter().fold(0i64, |acc, &d| acc * 10 + d as i64)
}

/// # Example
/// ```
/// let input = "987654321111111\n811111111111119\n234234234234278\n818181911112111";
/// assert_eq!(part_a(input.to_string()), "357");
/// ```
fn part_a(s: String) -> String {
    let mut sum: i64 = 0;
    for line in s.split("\n") {
        let digits: Vec<u8> = line.bytes().map(|b| b - b'0').collect();
        let best = largest_subsequence(&digits, 2);
        sum += digits_to_number(&best);
    }
    sum.to_string()
}

fn part_b(s: String) -> String {
    let mut sum: i64 = 0;
    for line in s.split("\n") {
        let digits: Vec<u8> = line.bytes().map(|b| b - b'0').collect();
        let best = largest_subsequence(&digits, 12);
        sum += digits_to_number(&best);
    }
    sum.to_string()
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

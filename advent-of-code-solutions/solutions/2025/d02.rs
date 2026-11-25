// 2025 day 2: https://adventofcode.com/2025/day/2
#![allow(dead_code)]

/// ```
/// let s = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124";
/// assert_eq!(part_a(s.to_string()), "1227775554");
/// ```
/// Check if a number's digits repeat exactly twice (e.g. 1010 = "10"|"10").
///
/// # Examples
/// ```
/// assert!(day_2025_02::is_twice_repeating(99));
/// assert!(day_2025_02::is_twice_repeating(1010));
/// assert!(day_2025_02::is_twice_repeating(1188511885));
/// assert!(day_2025_02::is_twice_repeating(222222));
/// assert!(!day_2025_02::is_twice_repeating(1698522));
/// assert!(day_2025_02::is_twice_repeating(446446));
/// assert!(!day_2025_02::is_twice_repeating(111));
/// ```
fn is_twice_repeating(n: i64) -> bool {
    let mut digits = 0u32;
    let mut tmp = n;
    while tmp > 0 {
        digits += 1;
        tmp /= 10;
    }
    if digits % 2 != 0 {
        return false;
    }
    let divisor = 10i64.pow(digits / 2) + 1;
    n % divisor == 0
}

fn part_a(s: String) -> String {
    let mut sum = 0;
    for line in s.split(",") {
        let parts: Vec<&str> = line.split("-").collect();
        let a = parts[0].parse::<i64>().unwrap();
        let b = parts[1].parse::<i64>().unwrap();
        for i in a..=b {
            if is_twice_repeating(i) {
                sum += i;
            }
        }
    }
    sum.to_string()
}

/// Check if digits are composed of a substring repeated at least twice.
///
/// # Examples
/// ```
/// assert!(day_2025_02::check_for_repeating_digits(&[9, 9]));
/// assert!(day_2025_02::check_for_repeating_digits(&[1, 0, 1, 0]));
/// assert!(day_2025_02::check_for_repeating_digits(&[1, 1, 8, 8, 5, 1, 1, 8, 8, 5]));
/// assert!(day_2025_02::check_for_repeating_digits(&[2, 2, 2, 2, 2, 2]));
/// assert!(!day_2025_02::check_for_repeating_digits(&[1, 6, 9, 8, 5, 2, 2]));
/// assert!(day_2025_02::check_for_repeating_digits(&[4, 4, 6, 4, 4, 6]));
/// assert!(day_2025_02::check_for_repeating_digits(&[1, 1, 1]));
/// assert!(!day_2025_02::check_for_repeating_digits(&[1, 1, 2]));
/// ```
fn check_for_repeating_digits(cs: &[u8]) -> bool {
    let n = cs.len();
    for period in 1..=n / 2 {
        if n % period != 0 || cs[period] != cs[0] {
            continue;
        }
        if (0..n).all(|i| cs[i] == cs[i % period]) {
            return true;
        }
    }
    false
}

fn write_digits(n: i64, buf: &mut [u8; 20]) -> usize {
    let mut tmp = n;
    let mut len = 0;
    while tmp > 0 {
        len += 1;
        buf[20 - len] = (tmp % 10) as u8;
        tmp /= 10;
    }
    len
}

fn part_b(s: String) -> String {
    let mut sum: i64 = 0;
    let mut buf = [0u8; 20];
    for line in s.split(",") {
        let parts: Vec<&str> = line.split("-").collect();
        let a = parts[0].parse::<i64>().unwrap();
        let b = parts[1].parse::<i64>().unwrap();
        for i in a..=b {
            let len = write_digits(i, &mut buf);
            if check_for_repeating_digits(&buf[20 - len..]) {
                sum += i;
            }
        }
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

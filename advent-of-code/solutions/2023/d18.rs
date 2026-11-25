// 2023 day 18: https://adventofcode.com/2023/day/18
#![allow(dead_code)]

/// Solve day 18 part A: Lavaduct Lagoon volume.
///
/// # Example
/// ```
/// let input = "\
/// R 6 (#70c710)
/// D 5 (#0dc571)
/// L 2 (#5713f0)
/// D 2 (#d2c081)
/// R 2 (#59c680)
/// D 2 (#411b91)
/// L 5 (#8ceee2)
/// U 2 (#caa173)
/// L 1 (#1b58a2)
/// U 2 (#caa171)
/// R 2 (#7807d2)
/// U 3 (#a77fa3)
/// L 2 (#015232)
/// U 2 (#7a21e3)";
/// assert_eq!(part_a(input.to_string()), "62");
/// ```
fn part_a(s: String) -> String {
    let mut points: Vec<(i64, i64)> = Vec::new();
    let mut current = (0, 0);
    points.push(current);
    let mut perimeter = 0;

    for line in s.lines() {
        let parts: Vec<&str> = line.split_whitespace().collect();
        let dir = parts[0];
        let dist: i64 = parts[1].parse().unwrap();

        match dir {
            "U" => current.0 -= dist,
            "D" => current.0 += dist,
            "L" => current.1 -= dist,
            "R" => current.1 += dist,
            _ => panic!("Invalid direction"),
        }
        points.push(current);
        perimeter += dist;
    }

    // Shoelace formula
    let mut area = 0;
    for i in 0..points.len() - 1 {
        area += points[i].0 * points[i + 1].1 - points[i + 1].0 * points[i].1;
    }
    area = area.abs() / 2;

    // Pick's theorem: A = i + b/2 - 1
    // We want the total area covered by the lagoon, which is the number of integer points inside (i)
    // plus the number of integer points on the boundary (b).
    // i + b = (A - b/2 + 1) + b = A + b/2 + 1
    let result = area + perimeter / 2 + 1;
    result.to_string()
}

fn part_b(_s: String) -> String {
    "0".to_string()
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

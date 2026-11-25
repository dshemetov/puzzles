// 2025 day 8: https://adventofcode.com/2025/day/8
#![allow(dead_code)]

/// # Example
/// ```
/// let input = "162,817,812\n57,618,57\n906,360,560\n592,479,940\n352,342,300\n466,668,158\n542,29,236\n431,825,988\n739,650,466\n52,470,668\n216,146,977\n819,987,18\n117,168,530\n805,96,715\n346,949,466\n970,615,88\n941,993,340\n862,61,35\n984,92,344\n425,690,689";
/// assert_eq!(day_2025_08::solve(&input.to_string(), 10), "40");
/// ```
fn solve(s: &str, iterations: usize) -> String {
    let points: Vec<(i64, i64, i64)> = s
        .lines()
        .map(|l| {
            let p: Vec<i64> = l.split(',').map(|t| t.parse().unwrap()).collect();
            (p[0], p[1], p[2])
        })
        .collect();
    let n = points.len();

    // All pairs sorted by squared Euclidean distance (preserves ordering)
    let mut pairs: Vec<(u64, usize, usize)> = Vec::with_capacity(n * (n - 1) / 2);
    for i in 0..n {
        for j in (i + 1)..n {
            let dx = points[i].0 - points[j].0;
            let dy = points[i].1 - points[j].1;
            let dz = points[i].2 - points[j].2;
            pairs.push(((dx * dx + dy * dy + dz * dz) as u64, i, j));
        }
    }
    pairs.sort_unstable();

    // Union-Find
    let mut parent: Vec<usize> = (0..n).collect();
    let mut size: Vec<usize> = vec![1; n];

    fn find(parent: &mut [usize], x: usize) -> usize {
        if parent[x] != x {
            parent[x] = find(parent, parent[x]);
        }
        parent[x]
    }

    for &(_, i, j) in pairs.iter().take(iterations) {
        let ri = find(&mut parent, i);
        let rj = find(&mut parent, j);
        if ri == rj {
            continue;
        }
        if size[ri] < size[rj] {
            parent[ri] = rj;
            size[rj] += size[ri];
        } else {
            parent[rj] = ri;
            size[ri] += size[rj];
        }
    }

    let mut set_sizes: Vec<u64> = (0..n)
        .filter(|&i| find(&mut parent, i) == i)
        .map(|i| size[i] as u64)
        .collect();
    set_sizes.sort_unstable_by(|a, b| b.cmp(a));
    set_sizes.iter().take(3).product::<u64>().to_string()
}

fn part_a(s: String) -> String {
    solve(&s, 1000)
}

/// # Example
/// ```
/// let input = "162,817,812\n57,618,57\n906,360,560\n592,479,940\n352,342,300\n466,668,158\n542,29,236\n431,825,988\n739,650,466\n52,470,668\n216,146,977\n819,987,18\n117,168,530\n805,96,715\n346,949,466\n970,615,88\n941,993,340\n862,61,35\n984,92,344\n425,690,689";
/// assert_eq!(part_b(input.to_string()), "25272");
/// ```
fn part_b(s: String) -> String {
    let points: Vec<(i64, i64, i64)> = s
        .lines()
        .map(|l| {
            let p: Vec<i64> = l.split(',').map(|t| t.parse().unwrap()).collect();
            (p[0], p[1], p[2])
        })
        .collect();
    let n = points.len();

    let mut pairs: Vec<(u64, usize, usize)> = Vec::with_capacity(n * (n - 1) / 2);
    for i in 0..n {
        for j in (i + 1)..n {
            let dx = points[i].0 - points[j].0;
            let dy = points[i].1 - points[j].1;
            let dz = points[i].2 - points[j].2;
            pairs.push(((dx * dx + dy * dy + dz * dz) as u64, i, j));
        }
    }
    pairs.sort_unstable();

    let mut parent: Vec<usize> = (0..n).collect();
    let mut size: Vec<usize> = vec![1; n];

    fn find(parent: &mut [usize], x: usize) -> usize {
        if parent[x] != x {
            parent[x] = find(parent, parent[x]);
        }
        parent[x]
    }

    let mut components = n;
    for &(_, i, j) in &pairs {
        let ri = find(&mut parent, i);
        let rj = find(&mut parent, j);
        if ri == rj {
            continue;
        }
        if size[ri] < size[rj] {
            parent[ri] = rj;
            size[rj] += size[ri];
        } else {
            parent[rj] = ri;
            size[ri] += size[rj];
        }
        components -= 1;
        if components == 1 {
            return (points[i].0 * points[j].0).to_string();
        }
    }
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

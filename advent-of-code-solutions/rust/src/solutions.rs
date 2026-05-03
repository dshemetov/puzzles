// Mono-file of all solutions for now.

#[allow(unused_variables)]
#[allow(dead_code)]
pub mod template {
    pub fn a(s: String) -> String {
        "0".to_string()
    }

    pub fn b(s: String) -> String {
        "0".to_string()
    }
}

pub mod day_2023_17 {
    use std::cmp::Ordering;
    use std::collections::{BinaryHeap, HashMap};

    #[derive(Copy, Clone, Eq, PartialEq, Hash, Debug)]
    enum Dir {
        Up,
        Down,
        Left,
        Right,
    }

    impl Dir {
        fn reverse(&self) -> Dir {
            match self {
                Dir::Up => Dir::Down,
                Dir::Down => Dir::Up,
                Dir::Left => Dir::Right,
                Dir::Right => Dir::Left,
            }
        }

        fn apply(&self, r: usize, c: usize, rows: usize, cols: usize) -> Option<(usize, usize)> {
            match self {
                Dir::Up if r > 0 => Some((r - 1, c)),
                Dir::Down if r + 1 < rows => Some((r + 1, c)),
                Dir::Left if c > 0 => Some((r, c - 1)),
                Dir::Right if c + 1 < cols => Some((r, c + 1)),
                _ => None,
            }
        }
    }

    #[derive(Copy, Clone, Eq, PartialEq)]
    struct State {
        cost: u32,
        pos: (usize, usize),
        dir: Dir,
        consecutive: u8,
    }

    impl Ord for State {
        fn cmp(&self, other: &Self) -> Ordering {
            other.cost.cmp(&self.cost)
        }
    }

    impl PartialOrd for State {
        fn partial_cmp(&self, other: &Self) -> Option<Ordering> {
            Some(self.cmp(other))
        }
    }

    fn solve_pathfinding(s: String, min_consecutive: u8, max_consecutive: u8) -> String {
        let grid: Vec<Vec<u32>> = s
            .lines()
            .map(|line| line.chars().map(|c| c.to_digit(10).unwrap()).collect())
            .collect();

        let rows = grid.len();
        let cols = grid[0].len();

        let mut heap = BinaryHeap::new();
        let mut visited = HashMap::new();

        // Start with two possible initial directions
        heap.push(State {
            cost: 0,
            pos: (0, 0),
            dir: Dir::Right,
            consecutive: 0,
        });
        heap.push(State {
            cost: 0,
            pos: (0, 0),
            dir: Dir::Down,
            consecutive: 0,
        });

        while let Some(State {
            cost,
            pos,
            dir,
            consecutive,
        }) = heap.pop()
        {
            // For part B, need to satisfy min_consecutive before stopping
            if pos == (rows - 1, cols - 1) && consecutive >= min_consecutive {
                return cost.to_string();
            }

            let key = (pos, dir, consecutive);
            if visited.contains_key(&key) {
                continue;
            }
            visited.insert(key, cost);

            for next_dir in [Dir::Up, Dir::Down, Dir::Left, Dir::Right] {
                // Can't reverse
                if next_dir == dir.reverse() {
                    continue;
                }

                // Must go straight for min_consecutive before turning
                if next_dir != dir && consecutive < min_consecutive {
                    continue;
                }

                let next_consecutive = if next_dir == dir { consecutive + 1 } else { 1 };

                // Can't go straight more than max_consecutive times
                if next_consecutive > max_consecutive {
                    continue;
                }

                if let Some((nr, nc)) = next_dir.apply(pos.0, pos.1, rows, cols) {
                    let next_cost = cost + grid[nr][nc];
                    heap.push(State {
                        cost: next_cost,
                        pos: (nr, nc),
                        dir: next_dir,
                        consecutive: next_consecutive,
                    });
                }
            }
        }

        "0".to_string()
    }

    /// Solve day 17 part A: path-finding with movement constraints.
    ///
    /// # Example
    /// ```
    /// # use advent::solutions::day_2023_17;
    /// let input = "\
    /// 2413432311323
    /// 3215453535623
    /// 3255245654254
    /// 3446585845452
    /// 4546657867536
    /// 1438598798454
    /// 4457876987766
    /// 3637877979653
    /// 4654967986887
    /// 4564679986453
    /// 1224686865563
    /// 2546548887735
    /// 4322674655533";
    /// assert_eq!(day_2023_17::a(input.to_string()), "102");
    /// ```
    pub fn a(s: String) -> String {
        solve_pathfinding(s, 0, 3)
    }

    /// Solve day 17 part B: path-finding with movement constraints.
    ///
    /// # Example
    /// ```
    /// # use advent::solutions::day_2023_17;
    /// let input = "\
    /// 2413432311323
    /// 3215453535623
    /// 3255245654254
    /// 3446585845452
    /// 4546657867536
    /// 1438598798454
    /// 4457876987766
    /// 3637877979653
    /// 4654967986887
    /// 4564679986453
    /// 1224686865563
    /// 2546548887735
    /// 4322674655533";
    /// assert_eq!(day_2023_17::b(input.to_string()), "94");
    /// ```
    pub fn b(s: String) -> String {
        solve_pathfinding(s, 4, 10)
    }
}

pub mod day_2023_18 {
    /// Solve day 18 part A: Lavaduct Lagoon volume.
    ///
    /// # Example
    /// ```
    /// # use advent::solutions::day_2023_18;
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
    /// assert_eq!(day_2023_18::a(input.to_string()), "62");
    /// ```
    pub fn a(s: String) -> String {
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

    pub fn b(_s: String) -> String {
        "0".to_string()
    }
}

pub mod day_2025_01 {
    fn parse_event(e: &str) -> i32 {
        let (sign, rest) = e.split_at(1);
        let magnitude: i32 = rest.parse().unwrap();
        match sign {
            "R" => magnitude,
            "L" => -magnitude,
            _ => panic!("Invalid direction"),
        }
    }

    pub fn a(s: String) -> String {
        let (_, count) = s.lines().fold((50, 0), |(val, count), e| {
            let nval = (val + parse_event(e)) % 100;
            (nval, count + if nval == 0 { 1 } else { 0 })
        });
        count.to_string()
    }

    pub fn b(s: String) -> String {
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
}

pub mod day_2025_02 {
    /// ```
    /// # use advent::solutions::day_2025_02;
    /// let s = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124";
    /// assert_eq!(day_2025_02::a(s.to_string()), "1227775554");
    /// ```
    /// Check if a number's digits repeat exactly twice (e.g. 1010 = "10"|"10").
    ///
    /// # Examples
    /// ```
    /// # use advent::solutions::day_2025_02;
    /// assert!(day_2025_02::is_twice_repeating(99));
    /// assert!(day_2025_02::is_twice_repeating(1010));
    /// assert!(day_2025_02::is_twice_repeating(1188511885));
    /// assert!(day_2025_02::is_twice_repeating(222222));
    /// assert!(!day_2025_02::is_twice_repeating(1698522));
    /// assert!(day_2025_02::is_twice_repeating(446446));
    /// assert!(!day_2025_02::is_twice_repeating(111));
    /// ```
    pub fn is_twice_repeating(n: i64) -> bool {
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

    pub fn a(s: String) -> String {
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
    /// # use advent::solutions::day_2025_02;
    /// assert!(day_2025_02::check_for_repeating_digits(&[9, 9]));
    /// assert!(day_2025_02::check_for_repeating_digits(&[1, 0, 1, 0]));
    /// assert!(day_2025_02::check_for_repeating_digits(&[1, 1, 8, 8, 5, 1, 1, 8, 8, 5]));
    /// assert!(day_2025_02::check_for_repeating_digits(&[2, 2, 2, 2, 2, 2]));
    /// assert!(!day_2025_02::check_for_repeating_digits(&[1, 6, 9, 8, 5, 2, 2]));
    /// assert!(day_2025_02::check_for_repeating_digits(&[4, 4, 6, 4, 4, 6]));
    /// assert!(day_2025_02::check_for_repeating_digits(&[1, 1, 1]));
    /// assert!(!day_2025_02::check_for_repeating_digits(&[1, 1, 2]));
    /// ```
    pub fn check_for_repeating_digits(cs: &[u8]) -> bool {
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

    pub fn b(s: String) -> String {
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
}

pub mod day_2025_03 {
    /// ```
    /// # use advent::solutions::day_2025_03;
    /// let digits: Vec<u8> = "234234234234278".bytes().map(|b| b - b'0').collect();
    /// let expected: Vec<u8> = "434234234278".bytes().map(|b| b - b'0').collect();
    /// assert_eq!(day_2025_03::largest_subsequence(&digits, 12), expected);
    /// ```
    pub fn largest_subsequence(digits: &[u8], k: usize) -> Vec<u8> {
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
    /// # use advent::solutions::day_2025_03;
    /// let input = "987654321111111\n811111111111119\n234234234234278\n818181911112111";
    /// assert_eq!(day_2025_03::a(input.to_string()), "357");
    /// ```
    pub fn a(s: String) -> String {
        let mut sum: i64 = 0;
        for line in s.split("\n") {
            let digits: Vec<u8> = line.bytes().map(|b| b - b'0').collect();
            let best = largest_subsequence(&digits, 2);
            sum += digits_to_number(&best);
        }
        sum.to_string()
    }

    pub fn b(s: String) -> String {
        let mut sum: i64 = 0;
        for line in s.split("\n") {
            let digits: Vec<u8> = line.bytes().map(|b| b - b'0').collect();
            let best = largest_subsequence(&digits, 12);
            sum += digits_to_number(&best);
        }
        sum.to_string()
    }
}

pub mod day_2025_04 {
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
    /// # use advent::solutions::day_2025_04;
    /// let input = "..@@.@@@@.\n@@@.@.@.@@\n@@@@@.@.@@\n@.@@@@..@.\n@@.@@@@.@@\n.@@@@@@@.@\n.@.@.@.@@@\n@.@@@.@@@@\n.@@@@@@@@.\n@.@.@@@.@.";
    /// assert_eq!(day_2025_04::a(input.to_string()), "13");
    /// ```
    pub fn a(s: String) -> String {
        let rows = s.lines().count();
        let cols = s.lines().next().unwrap().len();
        let grid: Vec<u8> = s.lines().flat_map(|l| l.bytes()).collect();
        (0..grid.len())
            .filter(|&i| grid[i] == b'@' && count_neighbors(&grid, cols, rows, i) < 4)
            .count()
            .to_string()
    }

    pub fn b(s: String) -> String {
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
}

pub mod day_2025_05 {
    /// # Example
    /// ```
    /// # use advent::solutions::day_2025_05;
    /// let input = "3-5\n10-14\n16-20\n12-18\n\n1\n5\n8\n11\n17\n32";
    /// assert_eq!(day_2025_05::a(input.to_string()), "3");
    /// ```
    pub fn a(s: String) -> String {
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
    /// # use advent::solutions::day_2025_05;
    /// let input = "3-5\n10-14\n16-20\n12-18\n\n1\n5\n8\n11\n17\n32";
    /// assert_eq!(day_2025_05::b(input.to_string()), "14");
    /// ```
    pub fn b(s: String) -> String {
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
}

pub mod day_2025_06 {
    /// # Example
    /// ```
    /// # use advent::solutions::day_2025_06;
    /// let input = "123 328  51 64\n 45 64  387 23\n  6 98  215 314\n*   +   *   +";
    /// assert_eq!(day_2025_06::a(input.to_string()), "4277556");
    /// ```
    pub fn a(s: String) -> String {
        let lines: Vec<&str> = s.lines().collect();
        let ops: Vec<&str> = lines.last().unwrap().split_whitespace().collect();
        let num_cols = ops.len();
        let mut cols = vec![Vec::new(); num_cols];
        for line in &lines[..lines.len() - 1] {
            for (i, tok) in line.split_whitespace().enumerate() {
                cols[i].push(tok.parse::<i64>().unwrap());
            }
        }
        cols.iter()
            .zip(ops.iter())
            .map(|(col, &op)| match op {
                "+" => col.iter().sum::<i64>(),
                "*" => col.iter().product::<i64>(),
                _ => panic!("Unknown op: {}", op),
            })
            .sum::<i64>()
            .to_string()
    }

    /// # Example
    /// ```
    /// # use advent::solutions::day_2025_06;
    /// let input = "123 328  51 64\n 45 64  387 23\n  6 98  215 314\n*   +   *   +  ";
    /// assert_eq!(day_2025_06::b(input.to_string()), "3263827");
    /// ```
    pub fn b(s: String) -> String {
        let lines: Vec<&str> = s.lines().collect();
        let op_line = lines.last().unwrap();
        let data_lines: Vec<&[u8]> = lines[..lines.len() - 1]
            .iter()
            .map(|l| l.as_bytes())
            .collect();
        let width = lines.iter().map(|l| l.len()).max().unwrap();

        // Build vertical strings for each character column
        let col_strings: Vec<String> = (0..width)
            .map(|c| {
                data_lines
                    .iter()
                    .map(|row| if c < row.len() { row[c] as char } else { ' ' })
                    .filter(|ch| ch.is_ascii_digit())
                    .collect()
            })
            .collect();

        // Find operations and their column positions
        let ops: Vec<(usize, u8)> = op_line
            .bytes()
            .enumerate()
            .filter(|&(_, b)| b == b'*' || b == b'+')
            .collect();

        // Group columns by operation, parse numbers, apply
        ops.iter()
            .enumerate()
            .map(|(oi, &(start, op))| {
                let end = if oi + 1 < ops.len() {
                    ops[oi + 1].0
                } else {
                    width
                };
                let numbers: Vec<i64> = col_strings[start..end]
                    .iter()
                    .filter(|s| !s.is_empty())
                    .map(|s| s.parse().unwrap())
                    .collect();
                match op {
                    b'+' => numbers.iter().sum::<i64>(),
                    b'*' => numbers.iter().product::<i64>(),
                    _ => unreachable!(),
                }
            })
            .sum::<i64>()
            .to_string()
    }
}

pub mod day_2025_07 {
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
    /// # use advent::solutions::day_2025_07;
    /// let input = ".......S.......\n...............\n.......^.......\n...............\n......^.^......\n...............\n.....^.^.^.....\n...............\n....^.^...^....\n...............\n...^.^...^.^...\n...............\n..^...^.....^..\n...............\n.^.^.^.^.^...^.\n................";
    /// assert_eq!(day_2025_07::a(input.to_string()), "21");
    /// ```
    pub fn a(s: String) -> String {
        solve_splits(&s).to_string()
    }

    pub fn b(s: String) -> String {
        solve_paths(&s).to_string()
    }
}

pub mod day_2025_08 {
    /// # Example
    /// ```
    /// # use advent::solutions::day_2025_08;
    /// let input = "162,817,812\n57,618,57\n906,360,560\n592,479,940\n352,342,300\n466,668,158\n542,29,236\n431,825,988\n739,650,466\n52,470,668\n216,146,977\n819,987,18\n117,168,530\n805,96,715\n346,949,466\n970,615,88\n941,993,340\n862,61,35\n984,92,344\n425,690,689";
    /// assert_eq!(day_2025_08::solve(&input.to_string(), 10), "40");
    /// ```
    pub fn solve(s: &str, iterations: usize) -> String {
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

    pub fn a(s: String) -> String {
        solve(&s, 1000)
    }

    /// # Example
    /// ```
    /// # use advent::solutions::day_2025_08;
    /// let input = "162,817,812\n57,618,57\n906,360,560\n592,479,940\n352,342,300\n466,668,158\n542,29,236\n431,825,988\n739,650,466\n52,470,668\n216,146,977\n819,987,18\n117,168,530\n805,96,715\n346,949,466\n970,615,88\n941,993,340\n862,61,35\n984,92,344\n425,690,689";
    /// assert_eq!(day_2025_08::b(input.to_string()), "25272");
    /// ```
    pub fn b(s: String) -> String {
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
}

pub mod day_2025_09 {
    fn parse(s: &str) -> Vec<(i64, i64)> {
        s.lines()
            .map(|l| {
                let mut sp = l.split(',');
                let x: i64 = sp.next().unwrap().parse().unwrap();
                let y: i64 = sp.next().unwrap().parse().unwrap();
                (x, y)
            })
            .collect()
    }

    /// # Example
    /// ```
    /// # use advent::solutions::day_2025_09;
    /// let input = "7,1\n11,1\n11,7\n9,7\n9,5\n2,5\n2,3\n7,3";
    /// assert_eq!(day_2025_09::a(input.to_string()), "50");
    /// ```
    pub fn a(s: String) -> String {
        let pts = parse(&s);
        let mut best = 0i64;
        for i in 0..pts.len() {
            for j in (i + 1)..pts.len() {
                let area = ((pts[i].0 - pts[j].0).abs() + 1) * ((pts[i].1 - pts[j].1).abs() + 1);
                best = best.max(area);
            }
        }
        best.to_string()
    }

    fn point_in_polygon(px: f64, py: f64, poly: &[(i64, i64)]) -> bool {
        let n = poly.len();
        let mut inside = false;
        let mut j = n - 1;
        for i in 0..n {
            let (xi, yi) = (poly[i].0 as f64, poly[i].1 as f64);
            let (xj, yj) = (poly[j].0 as f64, poly[j].1 as f64);
            if ((yi > py) != (yj > py)) && (px < (xj - xi) * (py - yi) / (yj - yi) + xi) {
                inside = !inside;
            }
            j = i;
        }
        inside
    }

    // Cross product of vectors OA and OB.
    fn cross(ox: i64, oy: i64, ax: i64, ay: i64, bx: i64, by: i64) -> i64 {
        (ax - ox) * (by - oy) - (ay - oy) * (bx - ox)
    }

    // True if segments AB and CD intersect at a point interior to both (not at endpoints).
    // If d1 and d2 have opposite signs, then A and B are on opposite sides of line CD.
    // Similarly for d3 and d4.
    fn segments_properly_cross(a: (i64, i64), b: (i64, i64), c: (i64, i64), d: (i64, i64)) -> bool {
        let d1 = cross(c.0, c.1, d.0, d.1, a.0, a.1);
        let d2 = cross(c.0, c.1, d.0, d.1, b.0, b.1);
        let d3 = cross(a.0, a.1, b.0, b.1, c.0, c.1);
        let d4 = cross(a.0, a.1, b.0, b.1, d.0, d.1);
        ((d1 > 0 && d2 < 0) || (d1 < 0 && d2 > 0)) && ((d3 > 0 && d4 < 0) || (d3 < 0 && d4 > 0))
    }

    /// Check if an axis-aligned rectangle fits inside a rectilinear polygon on a discrete grid.
    fn rect_inside_polygon(x1: i64, y1: i64, x2: i64, y2: i64, poly: &[(i64, i64)]) -> bool {
        // 1. All four rectangle corners must be inside the polygon.
        // Add a small epsilon to inset the corners in the boundary.
        let eps = 0.25;
        let corners = [
            (x1 as f64 + eps, y1 as f64 + eps),
            (x2 as f64 - eps, y1 as f64 + eps),
            (x2 as f64 - eps, y2 as f64 - eps),
            (x1 as f64 + eps, y2 as f64 - eps),
        ];
        for &(cx, cy) in &corners {
            if point_in_polygon(cx, cy, poly) == false {
                return false;
            }
        }

        // 2. No polygon edge may properly cross any rectangle edge. We don't
        // exclude width-1 notches, since those don't show up in the input.
        let n = poly.len();
        let rect_edges = [
            ((x1, y1), (x2, y1)),
            ((x2, y1), (x2, y2)),
            ((x2, y2), (x1, y2)),
            ((x1, y2), (x1, y1)),
        ];
        for k in 0..n {
            let p1 = poly[k];
            let p2 = poly[(k + 1) % n];
            for &(ra, rb) in &rect_edges {
                if segments_properly_cross(p1, p2, ra, rb) {
                    return false;
                }
            }
        }

        true
    }

    /// # Examples
    /// ```
    /// # use advent::solutions::day_2025_09;
    /// let input = "7,1\n11,1\n11,7\n9,7\n9,5\n2,5\n2,3\n7,3";
    /// assert_eq!(day_2025_09::b(input.to_string()), "24");
    /// // Width-1 notch should not invalidate the full rectangle (discrete grid)
    /// let notch = "0,0\n5,0\n5,5\n4,5\n4,3\n3,3\n3,5\n0,5";
    /// assert_eq!(day_2025_09::b(notch.to_string()), "36");
    /// // Triangle example.
    /// let notch = "0,0\n2,0\n2,2\n5,2\n5,5\n0,5";
    /// assert_eq!(day_2025_09::b(notch.to_string()), "24");
    /// ```
    pub fn b(s: String) -> String {
        let pts = parse(&s);
        let n = pts.len();
        let mut best = 0i64;
        for i in 0..n {
            for j in (i + 1)..n {
                let x1 = pts[i].0.min(pts[j].0);
                let x2 = pts[i].0.max(pts[j].0);
                let y1 = pts[i].1.min(pts[j].1);
                let y2 = pts[i].1.max(pts[j].1);
                if x1 == x2 || y1 == y2 {
                    continue;
                }
                let area = (x2 - x1 + 1) * (y2 - y1 + 1);
                if area > best && rect_inside_polygon(x1, y1, x2, y2, &pts) {
                    best = area;
                }
            }
        }
        best.to_string()
    }
}

pub mod day_2025_10 {
    fn parse_line(line: &str) -> (u64, Vec<u64>, Vec<i64>) {
        let bracket_start = line.find('[').unwrap();
        let bracket_end = line.find(']').unwrap();
        let pattern = &line[bracket_start + 1..bracket_end];
        let mut target = 0u64;
        for (i, ch) in pattern.chars().enumerate() {
            if ch == '#' {
                target |= 1 << i;
            }
        }

        let rest = &line[bracket_end + 1..];
        // Parse {a,b,c,...} values
        let int_targets = if let Some(brace_start) = rest.find('{') {
            let brace_end = rest.find('}').unwrap();
            rest[brace_start + 1..brace_end]
                .split(',')
                .map(|t| t.trim().parse::<i64>().unwrap())
                .collect()
        } else {
            Vec::new()
        };

        let rest = rest.split('{').next().unwrap();

        let mut buttons = Vec::new();
        let bytes = rest.as_bytes();
        let mut i = 0;
        while i < bytes.len() {
            if bytes[i] == b'(' {
                let end = rest[i..].find(')').unwrap() + i;
                let inner = &rest[i + 1..end];
                let mut mask = 0u64;
                for tok in inner.split(',') {
                    let idx: usize = tok.trim().parse().unwrap();
                    mask |= 1 << idx;
                }
                buttons.push(mask);
                i = end + 1;
            } else {
                i += 1;
            }
        }

        (target, buttons, int_targets)
    }

    fn fmt_bits(val: u64, n: usize) -> String {
        (0..n)
            .map(|i| if val & (1 << i) != 0 { '1' } else { '0' })
            .collect()
    }

    macro_rules! dbg_print {
        ($debug:expr, $($arg:tt)*) => {
            if $debug { eprintln!($($arg)*); }
        };
    }

    /// Solve Ax = b over GF(2) for minimum Hamming weight x.
    fn min_presses(target: u64, buttons: &[u64], debug: bool) -> usize {
        let m = buttons.len();
        let n = 64
            - target.leading_zeros().min(
                buttons
                    .iter()
                    .map(|b| b.leading_zeros())
                    .min()
                    .unwrap_or(64),
            ) as usize;
        let n = n.max(1);

        let mut rows: Vec<(u64, u64)> = buttons
            .iter()
            .enumerate()
            .map(|(i, &b)| (b, 1u64 << i))
            .collect();

        dbg_print!(debug, "=== Target: {} ===", fmt_bits(target, n));
        dbg_print!(debug, "Initial matrix [pattern | contributors]:");
        if debug {
            for (i, &(pat, cont)) in rows.iter().enumerate() {
                dbg_print!(
                    debug,
                    "  btn {}: {} | {}",
                    i,
                    fmt_bits(pat, n),
                    fmt_bits(cont, m)
                );
            }
        }

        // Gaussian elimination over GF(2)
        let mut pivot_row = 0;
        let mut pivot_cols = Vec::new();
        for bit in 0..64 {
            let mut found = None;
            for r in pivot_row..m {
                if rows[r].0 & (1 << bit) != 0 {
                    found = Some(r);
                    break;
                }
            }
            if let Some(r) = found {
                rows.swap(pivot_row, r);
                for r2 in 0..m {
                    if r2 != pivot_row && rows[r2].0 & (1 << bit) != 0 {
                        rows[r2].0 ^= rows[pivot_row].0;
                        rows[r2].1 ^= rows[pivot_row].1;
                    }
                }
                if debug {
                    dbg_print!(debug, "\nPivot on bit {} (row {}):", bit, pivot_row);
                    for (i, &(pat, cont)) in rows.iter().enumerate() {
                        let marker = if i == pivot_row { " <-- pivot" } else { "" };
                        dbg_print!(
                            debug,
                            "  row {}: {} | {}{}",
                            i,
                            fmt_bits(pat, n),
                            fmt_bits(cont, m),
                            marker
                        );
                    }
                }
                pivot_cols.push((bit, pivot_row));
                pivot_row += 1;
            }
        }

        let rank = pivot_row;
        dbg_print!(
            debug,
            "\nReduced: rank={}, null space dim={}",
            rank,
            m - rank
        );

        // Express target in terms of reduced basis
        let mut remaining = target;
        let mut solution = 0u64;
        dbg_print!(debug, "\nSolving for target {}:", fmt_bits(target, n));
        for &(bit, row) in &pivot_cols {
            if remaining & (1 << bit) != 0 {
                remaining ^= rows[row].0;
                solution ^= rows[row].1;
                dbg_print!(
                    debug,
                    "  bit {} set -> XOR row {} -> remaining={}, solution={}",
                    bit,
                    row,
                    fmt_bits(remaining, n),
                    fmt_bits(solution, m)
                );
            }
        }

        if remaining != 0 {
            dbg_print!(debug, "  NO SOLUTION (remaining != 0)");
            return usize::MAX;
        }

        dbg_print!(
            debug,
            "\nParticular solution: {} (press {} buttons)",
            fmt_bits(solution, m),
            solution.count_ones()
        );

        // Null space: non-pivot rows with zero pattern but nonzero contributors
        let null_space: Vec<u64> = (rank..m).map(|r| rows[r].1).collect();
        let null_dim = null_space.len();

        if debug && null_dim > 0 {
            dbg_print!(debug, "Null space vectors:");
            for (i, &ns) in null_space.iter().enumerate() {
                dbg_print!(debug, "  ns {}: {}", i, fmt_bits(ns, m));
            }
        }

        let mut best = solution.count_ones() as usize;
        let limit = null_dim.min(20);
        for mask in 1..(1u64 << limit) {
            let mut alt = solution;
            for k in 0..limit {
                if mask & (1 << k) != 0 {
                    alt ^= null_space[k];
                }
            }
            let w = alt.count_ones() as usize;
            if w < best {
                dbg_print!(
                    debug,
                    "  Better solution via null mask {}: {} ({} presses)",
                    mask,
                    fmt_bits(alt, m),
                    w
                );
                best = w;
            }
        }

        dbg_print!(debug, "=> min presses = {}\n", best);
        best
    }

    /// # Example
    /// ```
    /// # use advent::solutions::day_2025_10;
    /// let input = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}";
    /// assert_eq!(day_2025_10::a(input.to_string()), "2");
    /// let input = "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}";
    /// assert_eq!(day_2025_10::a(input.to_string()), "3");
    /// let input = "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}";
    /// assert_eq!(day_2025_10::a(input.to_string()), "2");
    /// ```
    pub fn a(s: String) -> String {
        s.lines()
            .map(|line| {
                let (target, buttons, _int_targets) = parse_line(line);
                min_presses(target, &buttons, false)
            })
            .sum::<usize>()
            .to_string()
    }

    fn gcd(a: i64, b: i64) -> i64 {
        let (mut a, mut b) = (a.abs(), b.abs());
        while b != 0 {
            let t = b;
            b = a % b;
            a = t;
        }
        a
    }

    /// Solve Ax = b over non-negative integers, minimize sum(x).
    /// buttons[j] is a bitmask of which positions button j affects (+1 each).
    /// targets[i] is the required value at position i.
    fn min_presses2(targets: &[i64], buttons: &[u64], debug: bool) -> i64 {
        let n = targets.len();
        let m = buttons.len();

        // Build augmented matrix [A | b], n rows × (m+1) cols
        let mut mat: Vec<Vec<i64>> = (0..n)
            .map(|i| {
                let mut row = vec![0i64; m + 1];
                for j in 0..m {
                    if buttons[j] & (1 << i) != 0 {
                        row[j] = 1;
                    }
                }
                row[m] = targets[i];
                row
            })
            .collect();

        if debug {
            eprintln!("=== Integer system: {} positions, {} buttons ===", n, m);
            eprintln!("Targets: {:?}", targets);
            for (i, row) in mat.iter().enumerate() {
                eprintln!("  eq {}: {:?}", i, row);
            }
        }

        // --- Step 1: Gaussian elimination over Z ---
        fn normalize_row(row: &mut [i64]) {
            let g = row
                .iter()
                .copied()
                .map(|x| x.abs())
                .filter(|&x| x > 0)
                .fold(0i64, |a, b| gcd(a, b));
            if g > 1 {
                for x in row.iter_mut() {
                    *x /= g;
                }
            }
        }

        let mut pivot_cols: Vec<usize> = Vec::new();
        let mut row = 0;
        for col in 0..m {
            let mut pivot = None;
            for r in row..n {
                if mat[r][col] != 0 {
                    pivot = Some(r);
                    break;
                }
            }
            if let Some(p) = pivot {
                mat.swap(row, p);
                normalize_row(&mut mat[row]);
                if mat[row][col] < 0 {
                    for c in 0..=m {
                        mat[row][c] = -mat[row][c];
                    }
                }
                let pivot_val = mat[row][col];
                for r2 in 0..n {
                    if r2 != row && mat[r2][col] != 0 {
                        let factor = mat[r2][col];
                        for c in 0..=m {
                            mat[r2][c] = mat[r2][c] * pivot_val - factor * mat[row][c];
                        }
                        normalize_row(&mut mat[r2]);
                    }
                }
                pivot_cols.push(col);
                row += 1;
            }
        }
        let rank = row;

        // Check inconsistency
        for r in rank..n {
            if mat[r][m] != 0 {
                dbg_print!(debug, "No solution (inconsistent)");
                return i64::MAX;
            }
        }

        let free_cols: Vec<usize> = (0..m).filter(|c| !pivot_cols.contains(c)).collect();

        if debug {
            eprintln!("After elimination (rank={}):", rank);
            for (i, r) in mat[..rank].iter().enumerate() {
                eprintln!("  row {}: {:?}", i, r);
            }
            eprintln!("Pivot cols: {:?}, Free cols: {:?}", pivot_cols, free_cols);
        }

        // --- Step 2: Iterate over free variable values, evaluate pivot vars ---
        let max_val = *targets.iter().max().unwrap();
        let mut best = i64::MAX;

        fn try_free(
            mat: &[Vec<i64>],
            pivot_cols: &[usize],
            free_cols: &[usize],
            free_vals: &mut Vec<i64>,
            depth: usize,
            m: usize,
            max_val: i64,
            best: &mut i64,
            debug: bool,
        ) {
            if depth == free_cols.len() {
                let mut x = vec![0i64; m];
                for (i, &fval) in free_vals.iter().enumerate() {
                    x[free_cols[i]] = fval;
                }
                for (i, &pcol) in pivot_cols.iter().enumerate() {
                    let pivot_val = mat[i][pcol];
                    let mut rhs = mat[i][m];
                    for (j, &fcol) in free_cols.iter().enumerate() {
                        rhs -= mat[i][fcol] * free_vals[j];
                    }
                    if rhs % pivot_val != 0 {
                        return;
                    }
                    let val = rhs / pivot_val;
                    if val < 0 {
                        return;
                    }
                    x[pcol] = val;
                }
                let total: i64 = x.iter().sum();
                if total < *best {
                    if debug {
                        eprintln!("  Found: free={:?}, x={:?}, total={}", free_vals, x, total);
                    }
                    *best = total;
                }
                return;
            }

            for val in 0..=max_val {
                free_vals[depth] = val;
                try_free(mat, pivot_cols, free_cols, free_vals, depth + 1, m, max_val, best, debug);
            }
        }

        let mut free_vals = vec![0i64; free_cols.len()];
        try_free(
            &mat[..rank], &pivot_cols, &free_cols,
            &mut free_vals, 0, m, max_val, &mut best, debug,
        );

        dbg_print!(debug, "=> min presses (Z+) = {}\n", best);
        best
    }

    /// # Example
    /// ```
    /// # use advent::solutions::day_2025_10;
    /// let input = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}";
    /// assert_eq!(day_2025_10::b(input.to_string()), "10");
    /// let input = "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}";
    /// assert_eq!(day_2025_10::b(input.to_string()), "12");
    /// let input = "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}";
    /// assert_eq!(day_2025_10::b(input.to_string()), "11");
    /// let input = "[###....#..] (0,5,6) (0,2,3,4,6,9) (0,1,2,3,7,8) (0,1,4,5,9) (1,9) (1,2,3,5,6,7,9) (0,8) (3,7,8) (0,5,6,7,8) (3,4,6,7) (1,2,3,4,6,7,8,9) (1,7) {68,61,54,74,52,47,85,75,37,59}";
    /// assert_eq!(day_2025_10::b(input.to_string()), "127");
    /// ```
    pub fn b(s: String) -> String {
        s.lines()
            .map(|line| {
                let (_target, buttons, int_targets) = parse_line(line);
                min_presses2(&int_targets, &buttons, false)
            })
            .sum::<i64>()
            .to_string()
    }

    #[cfg(test)]
    mod tests {
        use super::*;

        #[test]
        fn debug_example_gf2() {
            let input = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}";
            let (target, buttons, _) = parse_line(input);
            assert_eq!(min_presses(target, &buttons, true), 2);
        }

        #[test]
        fn debug_example_int() {
            let input = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}";
            let (_, buttons, int_targets) = parse_line(input);
            let result = min_presses2(&int_targets, &buttons, true);
            eprintln!("Part b result: {}", result);
        }

        #[test]
        fn debug_big_example_int() {
            let input = "[###....#..] (0,5,6) (0,2,3,4,6,9) (0,1,2,3,7,8) (0,1,4,5,9) (1,9) (1,2,3,5,6,7,9) (0,8) (3,7,8) (0,5,6,7,8) (3,4,6,7) (1,2,3,4,6,7,8,9) (1,7) {68,61,54,74,52,47,85,75,37,59}";
            let (_, buttons, int_targets) = parse_line(input);
            let result = min_presses2(&int_targets, &buttons, true);
            eprintln!("Big example result: {}", result);
            assert_ne!(result, i64::MAX, "Should find a solution");
        }
    }
}

pub mod day_2025_11 {
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
    /// # use advent::solutions::day_2025_11;
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
    /// assert_eq!(day_2025_11::a(input.to_string()), "5");
    /// ```
    pub fn a(s: String) -> String {
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
    /// # use advent::solutions::day_2025_11;
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
    /// assert_eq!(day_2025_11::b(input.to_string()), "2");
    /// ```
    pub fn b(s: String) -> String {
        let graph = parse_graph(&s);
        let required = &["dac", "fft"];
        let mut memo = HashMap::new();
        let start_mask = if required.contains(&"svr") { 1u8 } else { 0u8 };
        count_paths_through("svr", start_mask, &graph, required, &mut memo).to_string()
    }
}

pub mod day_2025_12 {
    fn parse_input(s: &str) -> (Vec<usize>, Vec<(usize, usize, Vec<usize>)>) {
        let mut shape_sizes: Vec<usize> = Vec::new();
        let mut queries = Vec::new();
        let mut lines = s.lines().peekable();

        while let Some(line) = lines.peek() {
            let line = line.trim();
            if line.is_empty() {
                lines.next();
                continue;
            }
            // Query line: "WxH: n n n ..."
            if line.contains('x') && line.contains(':') {
                if let Some((dims, counts_str)) = line.split_once(':') {
                    if let Some((w_str, h_str)) = dims.trim().split_once('x') {
                        if let (Ok(w), Ok(h)) = (w_str.parse::<usize>(), h_str.parse::<usize>()) {
                            let counts: Vec<usize> = counts_str
                                .split_whitespace()
                                .map(|n| n.parse().unwrap())
                                .collect();
                            queries.push((w, h, counts));
                            lines.next();
                            continue;
                        }
                    }
                }
            }
            // Shape header: "N:"
            if let Some(idx_str) = line.strip_suffix(':') {
                if idx_str.trim().parse::<usize>().is_ok() {
                    lines.next();
                    let mut cell_count = 0;
                    while let Some(grid_line) = lines.peek() {
                        let grid_line = grid_line.trim();
                        if grid_line.is_empty() || grid_line.contains(':') {
                            break;
                        }
                        cell_count += grid_line.chars().filter(|&ch| ch == '#').count();
                        lines.next();
                    }
                    shape_sizes.push(cell_count);
                    continue;
                }
            }
            lines.next();
        }

        (shape_sizes, queries)
    }

    pub fn a(s: String) -> String {
        let (shape_sizes, queries) = parse_input(&s);
        queries
            .iter()
            .filter(|(w, h, counts)| {
                let total_cells: usize = counts
                    .iter()
                    .enumerate()
                    .map(|(i, &c)| c * shape_sizes[i])
                    .sum();
                total_cells <= w * h
            })
            .count()
            .to_string()
    }

    pub fn b(_s: String) -> String {
        "0".to_string()
    }

    #[cfg(test)]
    mod tests {
        use super::*;

        #[test]
        fn test_area_check() {
            let input = "0:\n#.#\n###\n\n1:\n##\n##\n\n6x3: 2 1\n3x2: 1 1";
            let result = a(input.to_string());
            // 2*5 + 1*4 = 14 <= 18 -> true; 1*5 + 1*4 = 9 > 6 -> false. 1 feasible.
            assert_eq!(result, "1");
        }
    }
}

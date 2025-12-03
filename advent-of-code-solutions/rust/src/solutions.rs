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
    pub fn a(s: String) -> String {
        let mut val = 50;
        let mut count = 0;
        for e in s.split("\n") {
            let ev = e
                .replace("R", "+")
                .replace("L", "-")
                .parse::<i32>()
                .unwrap();
            val = (val + ev) % 100;
            if val == 0 {
                count += 1;
            }
        }
        return count.to_string();
    }

    pub fn b(s: String) -> String {
        let mut val = 50;
        let mut nval;
        let mut count = 0;
        for e in s.split("\n") {
            let ev = e
                .replace("R", "+")
                .replace("L", "-")
                .parse::<i32>()
                .unwrap();
            nval = (val + ev);
            if (val < 0 && nval >= 0) || (val > 0 && nval <= 0) {
                count += 1 + (nval.abs() / 100);
            } else {
                count += (nval.abs() / 100);
            }
            val = nval % 100;
        }
        return count.to_string();
    }
}

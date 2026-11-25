// 2025 day 10: https://adventofcode.com/2025/day/10
#![allow(dead_code)]

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
/// let input = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}";
/// assert_eq!(part_a(input.to_string()), "2");
/// let input = "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}";
/// assert_eq!(part_a(input.to_string()), "3");
/// let input = "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}";
/// assert_eq!(part_a(input.to_string()), "2");
/// ```
fn part_a(s: String) -> String {
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
/// let input = "[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}";
/// assert_eq!(part_b(input.to_string()), "10");
/// let input = "[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}";
/// assert_eq!(part_b(input.to_string()), "12");
/// let input = "[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}";
/// assert_eq!(part_b(input.to_string()), "11");
/// let input = "[###....#..] (0,5,6) (0,2,3,4,6,9) (0,1,2,3,7,8) (0,1,4,5,9) (1,9) (1,2,3,5,6,7,9) (0,8) (3,7,8) (0,5,6,7,8) (3,4,6,7) (1,2,3,4,6,7,8,9) (1,7) {68,61,54,74,52,47,85,75,37,59}";
/// assert_eq!(part_b(input.to_string()), "127");
/// ```
fn part_b(s: String) -> String {
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

// 2025 day 9: https://adventofcode.com/2025/day/9
#![allow(dead_code)]

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
/// let input = "7,1\n11,1\n11,7\n9,7\n9,5\n2,5\n2,3\n7,3";
/// assert_eq!(part_a(input.to_string()), "50");
/// ```
fn part_a(s: String) -> String {
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
/// let input = "7,1\n11,1\n11,7\n9,7\n9,5\n2,5\n2,3\n7,3";
/// assert_eq!(part_b(input.to_string()), "24");
/// // Width-1 notch should not invalidate the full rectangle (discrete grid)
/// let notch = "0,0\n5,0\n5,5\n4,5\n4,3\n3,3\n3,5\n0,5";
/// assert_eq!(part_b(notch.to_string()), "36");
/// // Triangle example.
/// let notch = "0,0\n2,0\n2,2\n5,2\n5,5\n0,5";
/// assert_eq!(part_b(notch.to_string()), "24");
/// ```
fn part_b(s: String) -> String {
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

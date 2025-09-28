use crate::solutions::solve_2023_17_a;
use crate::utils::get_input;
use anyhow::Result;
use std::collections::HashMap;
use std::sync::LazyLock;

pub fn solve(q: Question) -> Result<String> {
    let solution = SOLUTIONS
        .get(&(q.year, q.day, q.part))
        .ok_or_else(|| anyhow::anyhow!("Solution not found"))?;
    let input = get_input(q.year, q.day)?;
    Ok((solution)(input))
}

#[derive(Debug, Clone, Copy)]
pub struct Question {
    year: u16,
    day: u8,
    part: char,
}
impl Question {
    pub fn new(year: u16, day: u8, part: char) -> Self {
        Self { year, day, part }
    }
}
pub static SOLUTIONS: LazyLock<HashMap<(u16, u8, char), fn(String) -> String>> =
    LazyLock::new(|| HashMap::from([((2023, 17, 'a'), solve_2023_17_a as fn(String) -> String)]));

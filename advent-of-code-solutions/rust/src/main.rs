mod question;
mod solutions;
mod utils;

use anyhow::Result;
use question::{Question, solve};

fn main() -> Result<()> {
    print_solution(2023, 17, 'a')?;
    Ok(())
}

fn print_solution(year: u16, day: u8, part: char) -> Result<()> {
    println!(
        "{} {}: {}",
        year,
        day,
        solve(Question::new(year, day, part))?
    );
    Ok(())
}

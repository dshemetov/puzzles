mod runner;
mod solutions;
mod utils;

use anyhow::Result;
use runner::{all_questions, solve};

fn main() -> Result<()> {
    for question in all_questions() {
        let result = solve(question)?;
        println!(
            "{} {} {}: {} ({:.3}ms)",
            result.question.year,
            result.question.day,
            result.question.part,
            result.answer,
            result.duration.as_secs_f64() * 1000.0
        );
    }
    Ok(())
}

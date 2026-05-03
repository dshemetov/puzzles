mod runner;
mod solutions;
mod utils;

use anyhow::Result;
use runner::{all_questions, solve};
use std::env;

fn main() -> Result<()> {
    let args: Vec<String> = env::args().skip(1).collect();

    let filter: Option<(u16, Option<u8>)> = match args.len() {
        0 => None,
        1 => Some((args[0].parse()?, None)),
        _ => Some((args[0].parse()?, Some(args[1].parse()?))),
    };

    let questions = all_questions()
        .into_iter()
        .filter(|q| match filter {
            None => true,
            Some((year, None)) => q.year == year,
            Some((year, Some(day))) => q.year == year && q.day == day,
        })
        .collect::<Vec<_>>();

    if questions.is_empty() {
        anyhow::bail!("No solutions found for the given arguments");
    }

    for question in questions {
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

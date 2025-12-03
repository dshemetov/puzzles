use crate::solutions::*;
use crate::utils::get_input;
use anyhow::Result;
use std::collections::HashMap;
use std::sync::LazyLock;
use std::time::{Duration, Instant};

#[derive(Debug, Clone, Copy, Hash, PartialEq, Eq)]
pub struct Question {
    pub year: u16,
    pub day: u8,
    pub part: char,
}

impl Question {
    pub fn new(year: u16, day: u8, part: char) -> Self {
        Self { year, day, part }
    }
}

pub struct SolutionResult {
    pub question: Question,
    pub answer: String,
    pub duration: Duration,
}

type Solution = fn(String) -> String;

pub static SOLUTIONS: LazyLock<HashMap<Question, Solution>> = LazyLock::new(|| {
    HashMap::from([
        (Question::new(2023, 17, 'a'), day_2023_17::a as Solution),
        (Question::new(2023, 17, 'b'), day_2023_17::b as Solution),
        (Question::new(2023, 18, 'a'), day_2023_18::a as Solution),
        (Question::new(2023, 18, 'b'), day_2023_18::b as Solution),
        (Question::new(2025, 1, 'a'), day_2025_01::a as Solution),
        (Question::new(2025, 1, 'b'), day_2025_01::b as Solution),
    ])
});

pub fn all_questions() -> Vec<Question> {
    let mut questions: Vec<Question> = SOLUTIONS.keys().copied().collect();
    questions.sort_by_key(|q| (q.year, q.day, q.part));
    questions
}

pub fn solve(question: Question) -> Result<SolutionResult> {
    let solution = SOLUTIONS
        .get(&question)
        .ok_or_else(|| anyhow::anyhow!("Solution not found for {:?}", question))?;

    let input = get_input(question.year, question.day)?;
    let start = Instant::now();
    let answer = (solution)(input);
    let duration = start.elapsed();

    Ok(SolutionResult {
        question,
        answer,
        duration,
    })
}

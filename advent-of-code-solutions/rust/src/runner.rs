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
        (Question::new(2025, 2, 'a'), day_2025_02::a as Solution),
        (Question::new(2025, 2, 'b'), day_2025_02::b as Solution),
        (Question::new(2025, 3, 'a'), day_2025_03::a as Solution),
        (Question::new(2025, 3, 'b'), day_2025_03::b as Solution),
        (Question::new(2025, 4, 'a'), day_2025_04::a as Solution),
        (Question::new(2025, 4, 'b'), day_2025_04::b as Solution),
        (Question::new(2025, 5, 'a'), day_2025_05::a as Solution),
        (Question::new(2025, 5, 'b'), day_2025_05::b as Solution),
        (Question::new(2025, 6, 'a'), day_2025_06::a as Solution),
        (Question::new(2025, 6, 'b'), day_2025_06::b as Solution),
        (Question::new(2025, 7, 'a'), day_2025_07::a as Solution),
        (Question::new(2025, 7, 'b'), day_2025_07::b as Solution),
        (Question::new(2025, 8, 'a'), day_2025_08::a as Solution),
        (Question::new(2025, 8, 'b'), day_2025_08::b as Solution),
        (Question::new(2025, 9, 'a'), day_2025_09::a as Solution),
        (Question::new(2025, 9, 'b'), day_2025_09::b as Solution),
        (Question::new(2025, 10, 'a'), day_2025_10::a as Solution),
        (Question::new(2025, 10, 'b'), day_2025_10::b as Solution),
        (Question::new(2025, 11, 'a'), day_2025_11::a as Solution),
        (Question::new(2025, 11, 'b'), day_2025_11::b as Solution),
        (Question::new(2025, 12, 'a'), day_2025_12::a as Solution),
        (Question::new(2025, 12, 'b'), day_2025_12::b as Solution),
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

use anyhow::Result;
use std::collections::HashMap;
use std::env;
use std::fs;
use ureq::get;

pub fn get_input(year: u16, day: u8) -> Result<String> {
    let file = format!(".cache/inputs/{}_{}.txt", year, day);
    match fs::read_to_string(&file) {
        Ok(input) => Ok(input),
        Err(_) => {
            let input = fetch_input(year, day)?;
            let input = input.trim().to_string();
            cache_input(year, day, &input)?;
            Ok(input)
        }
    }
}

fn fetch_input(year: u16, day: u8) -> Result<String> {
    let _ = load_env();
    let token = env::var("AOC_TOKEN")?;
    let url = format!("https://adventofcode.com/{}/day/{}/input", year, day);
    let response = get(url)
        .header("Cookie", &format!("session={}", token))
        .call()?
        .into_body()
        .read_to_string()?;
    Ok(response)
}

fn cache_input(year: u16, day: u8, input: &String) -> Result<()> {
    let file_dir = ".cache/inputs";
    fs::create_dir_all(&file_dir)?;
    let file = format!("{}/{}_{}.txt", file_dir, year, day);
    fs::write(&file, input)?;
    Ok(())
}

fn load_env() -> Result<()> {
    // Simple impl, handles KEY=VALUE pairs.
    let env = fs::read_to_string("../.env")?;
    let tuples = env.split("\n").map(|s| s.split("=").collect::<Vec<&str>>());
    let hashmap: HashMap<String, String> = tuples
        .map(|t| (t[0].to_string(), t[1].to_string()))
        .collect();
    unsafe {
        for (key, value) in hashmap.iter() {
            env::set_var(key, value);
        }
    }
    Ok(())
}

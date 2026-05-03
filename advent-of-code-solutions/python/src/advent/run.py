import json
import os
import time
import traceback
from collections.abc import Callable
from datetime import date
from importlib import import_module
from pathlib import Path

import requests
import typer
from rich import print
from rich.table import Table

app = typer.Typer(name="Advent of Code Solution Runner", chain=True)
AnswerType = int | str | None
YearOption = typer.Option(date.today().year, "--year", "-y", help="The year of the problem.")
DayOption = typer.Option(None, "--day", "-d", help="The day of the problem.")
PartOption = typer.Option(None, "--part", "-p", help="The part of the problem.")

CACHE_DIR = Path(".cache")
INPUTS_DIR = CACHE_DIR / "inputs"
ANSWERS_FILE = CACHE_DIR / "answers.json"


def _load_answers() -> dict:
    if ANSWERS_FILE.exists():
        return json.loads(ANSWERS_FILE.read_text())
    return {}


def _save_answers(cache: dict) -> None:
    ANSWERS_FILE.parent.mkdir(parents=True, exist_ok=True)
    ANSWERS_FILE.write_text(json.dumps(cache, indent=2))


def _answer_key(year: int, day: int, part: str) -> str:
    return f"{year}.{day}.{part}"


def get_puzzle_input(year: int, day: int, token: str | None = None) -> str:
    if token is None:
        token = os.getenv("AOC_TOKEN")
    if token is None:
        raise RuntimeError("AOC_TOKEN not set; fetching problem inputs will not work.")

    cache_file = INPUTS_DIR / str(year) / f"day{day:02d}.txt"
    if cache_file.exists():
        return cache_file.read_text()

    if year < 2015:
        raise ValueError("Year outside valid range [2015, 2022].")
    if day < 1 or day > 31:
        raise ValueError("Day outside valid range [1, 31].")

    print(f"Downloading puzzle input for day {day}, year {year}...")
    request = requests.get(url=f"https://adventofcode.com/{year}/day/{day}/input", cookies={"session": token}, timeout=10)
    request.raise_for_status()

    if "Please don't repeatedly request this endpoint" in request.text:
        raise ValueError("Too many requests.")
    if "You don't seem to be solving the right level" in request.text:
        raise ValueError("You're not on that level yet.")
    if "Please log in" in request.text:
        raise ValueError("Invalid or unset session cookie.")

    cache_file.parent.mkdir(parents=True, exist_ok=True)
    cache_file.write_text(request.text)
    return request.text


def get_answer(year: int, day: int, part: str) -> tuple[AnswerType, float]:
    try:
        solution_module = import_module(f"advent.advent{year}.p{day:02d}")
        solution_method: Callable[[str], AnswerType] = getattr(solution_module, f"solve_{part}")
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError("Problem not implemented yet.") from e
    t = time.perf_counter()
    answer: AnswerType = solution_method(get_puzzle_input(year, day))
    time_taken = time.perf_counter() - t

    cache = _load_answers()
    cache[_answer_key(year, day, part)] = {"answer": answer, "time_taken": time_taken, "timestamp": time.time()}
    _save_answers(cache)

    return answer, time_taken


def get_answer_cache(year: int, day: int, part: str, clear_cache: bool) -> tuple[AnswerType, float, float]:
    cache = _load_answers()
    key = _answer_key(year, day, part)

    if not clear_cache and key in cache:
        entry = cache[key]
        return entry["answer"], 0, entry["time_taken"]

    prev_time_taken = float("nan")
    if clear_cache and key in cache:
        prev_answer = cache[key]["answer"]
        prev_time_taken = cache[key]["time_taken"]
        answer, time_taken = get_answer(year, day, part)
        if answer != prev_answer:
            print(
                f"Warning, new result differs from cached for {year}.{day}.{part}.\n"
                f"New:{answer}.\nOld:{prev_answer}."
            )
    else:
        answer, time_taken = get_answer(year, day, part)

    return answer, time_taken, prev_time_taken


@app.command("solve")
def get_solutions(
    year: int = YearOption,
    day: int = DayOption,
    part: str = PartOption,
    clear_cache: bool = typer.Option(False, "--clear-cache", "-c", help="Clear the solution cache for this problem."),
    silent: bool = typer.Option(True, "--silent", "-s", help="Silence warnings."),
):
    """Prints the solution for a problem or problems."""
    days = range(1, 26) if day is None else [day]
    parts = ["a", "b"] if part is None else [part]
    total_time_taken = 0
    run_stats = {}
    for d in days:
        for p in parts:
            try:
                ans, time_taken, prev_time_taken = get_answer_cache(year, d, p, clear_cache)
            except ModuleNotFoundError:
                if not silent:
                    print(f"Problem {year}.{d}.{p} not implemented yet.")
                continue
            except Exception as e:
                print(f"Unexpected error occurred for {year}.{d}.{p}: {e}")
                traceback.print_exception(type(e), e, e.__traceback__)
                continue
            run_stats[(d, p)] = [ans, time_taken, prev_time_taken]
            total_time_taken += time_taken

    table = Table(
        title=f"{year} Solutions",
        caption=f"Total time taken: {total_time_taken:>5.3f}.",
    )
    table.add_column("Day", style="dim", no_wrap=True)
    table.add_column("Part", style="dim", no_wrap=True)
    table.add_column("Answer", justify="right")
    table.add_column("Time Taken", justify="right")
    table.add_column("Prev Time Taken", justify="right")

    for (d, p), (ans, time_taken, prev_time_taken) in run_stats.items():
        table.add_row(str(d), p, str(ans), f"{time_taken:>5.5f}", f"{prev_time_taken:>5.5f}")

    print(table)
    return table


@app.command("clear-download-cache")
def clear_download_cache(
    year: int = YearOption,
    day: int = DayOption,
):
    """Clears the input download cache."""
    days = range(1, 26) if day is None else [day]
    for d in days:
        cache_file = INPUTS_DIR / str(year) / f"day{d:02d}.txt"
        if cache_file.exists():
            cache_file.unlink()
            print(f"Download cache cleared for {year}.{d}.")
        else:
            print(f"No download cache for {year}.{d}.")


@app.command("clear-solution-cache")
def clear_solution_cache(
    year: int = YearOption,
    day: int = DayOption,
    part: str = PartOption,
):
    """Clears the solution cache."""
    cache = _load_answers()
    days = range(1, 26) if day is None else [day]
    parts = ["a", "b"] if part is None else [part]
    changed = False
    for d in days:
        for p in parts:
            key = _answer_key(year, d, p)
            if key in cache:
                del cache[key]
                changed = True
                print(f"Solution cache cleared for {year}.{d}.{p}.")
            else:
                print(f"No solution cache for {year}.{d}.{p}.")
    if changed:
        _save_answers(cache)


@app.command("make-table")
def make_table(year: int):
    """Makes a table of the run time statistics for a year and inserts into the README.md.

    TODO: Make this work.
    """
    get_solutions(year)


@app.command("generate-templates")
def generate_templates(year: int = YearOption, day: int = DayOption):
    """Generates templates for the given year."""
    days = range(1, 26) if day is None else [day]
    template_text = Path("src/advent/template.py").read_text()

    # Make directory if it doesn't exist
    Path(f"src/advent/advent{year}").mkdir(parents=True, exist_ok=True)

    # Generate templates
    for d in days:
        url = f"https://adventofcode.com/{year}/day/{d}"
        # r = requests.get(url)
        # r.raise_for_status()

        day_header = f'"""{d}. {url}"""\n\n'
        day_file = f"src/advent/advent{year}/p{d:02d}.py"
        if not Path(day_file).exists():
            Path(day_file).write_text(day_header + template_text)
            print(f"Generated {day_file}.")

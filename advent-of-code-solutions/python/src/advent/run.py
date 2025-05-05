import os
import time
import traceback
from datetime import date
from importlib import import_module
from pathlib import Path

import requests
import typer
from dotenv import load_dotenv, set_key
from joblib import Memory
from rich import print
from rich.table import Table

from .tools import get_puzzle_input

memory = Memory(".joblib_cache", verbose=0)
app = typer.Typer(name="Advent of Code Solution Runner", chain=True)

AnswerType = int | str | None
YearOption = typer.Option(date.today().year, "--year", "-y", help="The year of the problem.")
DayOption = typer.Option(None, "--day", "-d", help="The day of the problem.")
PartOption = typer.Option(None, "--part", "-p", help="The part of the problem.")


@memory.cache
def get_answer(year: int, day: int, part: str) -> tuple[AnswerType, float]:
    try:
        solution_module = import_module(f"advent.advent{year}.p{day:02d}")
        solution_method = getattr(solution_module, f"solve_{part}")
    except ModuleNotFoundError as e:
        raise ModuleNotFoundError("Problem not implemented yet.") from e
    t = time.perf_counter()
    answer = solution_method(get_puzzle_input(year, day))
    time_taken = time.perf_counter() - t
    return answer, time_taken


def get_answer_cache(year: int, day: int, part: str, clear_cache: bool) -> tuple[AnswerType, float, float]:
    if clear_cache:
        if get_answer.check_call_in_cache(year, day, part) is True:
            result = get_answer.call_and_shelve(year, day, part)
            prev_answer, prev_time_taken = result.get()
            result.clear()
            answer, time_taken = get_answer(year, day, part)
            if answer != prev_answer:
                print(
                    f"Warning, new result differs from cached for {year}.{day}.{part}.\n"
                    f"New:{answer}.\nOld:{prev_answer}."
                )
        else:
            answer, time_taken = get_answer(year, day, part)
            prev_time_taken = float("nan")
    else:
        answer, prev_time_taken = get_answer(year, day, part)
        time_taken = 0
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
    for day in days:
        for part in parts:
            try:
                ans, time_taken, prev_time_taken = get_answer_cache(year, day, part, clear_cache)
            except ModuleNotFoundError:
                if not silent:
                    print(f"Problem {year}.{day}.{part} not implemented yet.")
                continue
            except Exception as e:
                print(f"Unexpected error occurred for {year}.{day}.{part}: {e}")
                traceback.print_exception(type(e), e, e.__traceback__)
                continue
            run_stats[(day, part)] = [ans, time_taken, prev_time_taken]
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

    for (day, part), (ans, time_taken, prev_time_taken) in run_stats.items():
        table.add_row(str(day), part, str(ans), f"{time_taken:>5.5f}", f"{prev_time_taken:>5.5f}")

    print(table)
    return table


@app.command("set-cookie")
def set_cookie(
    cookie: str = typer.Option(
        "",
        "--cookie",
        "-c",
        help="The cookie to set.",
        prompt="Enter your cookie (input hidden)",
        hide_input=True,
    ),
):
    """Sets the cookie for the current user.

    Go to https://adventofcode.com/, inspect the browser session, and find your cookie.
    """
    set_key(".env", "AOC_TOKEN", cookie)


@app.command("clear-download-cache")
def clear_download_cache(
    year: int = YearOption,
    day: int = DayOption,
):
    """Clears the input download cache."""
    load_dotenv()
    AOC_TOKEN = os.environ.get("AOC_TOKEN")

    days = range(1, 26) if day is None else [day]
    for day in days:
        if get_puzzle_input.check_call_in_cache(year, day, AOC_TOKEN) is True:
            result = get_puzzle_input.call_and_shelve(year, day, AOC_TOKEN)
            result.clear()
            print(f"Download cache cleared for {year}.{day}.")
        else:
            print(f"No solution cache for {year}.{day}.")


@app.command("clear-solution-cache")
def clear_solution_cache(
    year: int = YearOption,
    day: int = DayOption,
    part: str = PartOption,
):
    """Clears the solution cache."""
    days = range(1, 26) if day is None else [day]
    parts = ["a", "b"] if part is None else [part]
    for day in days:
        for part in parts:
            if get_answer.check_call_in_cache(year, day, part) is True:
                result = get_answer.call_and_shelve(year, day, part)
                result.clear()
                print(f"Solution cache cleared for {year}.{day}.{part}.")
            else:
                print(f"No solution cache for {year}.{day}.{part}.")


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
    for day in days:
        url = f"https://adventofcode.com/{year}/day/{day}"
        # r = requests.get(url)
        # r.raise_for_status()

        day_header = f'"""{day}. {url}"""\n\n'
        day_file = f"src/advent/advent{year}/p{day:02d}.py"
        if not Path(day_file).exists():
            Path(day_file).write_text(day_header + template_text)
            print(f"Generated {day_file}.")

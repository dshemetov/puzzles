"""Leetcode CLI

Usage: uv run python leet.py get 34
"""

import ast
import json
import re
import time
from html.parser import HTMLParser
from pathlib import Path
from typing import Annotated, Optional

import requests
import typer

app = typer.Typer()

_BASE_URL = "https://leetcode.com"
_GRAPHQL_URL = f"{_BASE_URL}/graphql"
_HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://leetcode.com",
}

_CACHE_PATH = Path.home() / ".cache" / "leet" / "problems.json"
_CACHE_TTL = 24 * 60 * 60  # 24 hours


class _HTMLTextExtractor(HTMLParser):
    """Strip HTML tags, preserving newlines around block elements."""

    _BLOCK_TAGS = {"p", "div", "li", "br", "pre", "h1", "h2", "h3", "h4", "tr"}

    def __init__(self):
        super().__init__()
        self._parts: list[str] = []

    def handle_starttag(self, tag, attrs):
        if tag in self._BLOCK_TAGS:
            self._parts.append("\n")

    def handle_data(self, data):
        self._parts.append(data)

    def get_text(self) -> str:
        text = "".join(self._parts)
        # Collapse 3+ newlines to 2
        return re.sub(r"\n{3,}", "\n\n", text).strip()


def _strip_html(html: str) -> str:
    parser = _HTMLTextExtractor()
    parser.feed(html)
    return parser.get_text()


def _load_problems() -> list[dict]:
    if _CACHE_PATH.exists():
        cached = json.loads(_CACHE_PATH.read_text())
        if time.time() - cached["fetched_at"] < _CACHE_TTL:
            return cached["problems"]

    res = requests.get(f"{_BASE_URL}/api/problems/all/", headers=_HEADERS, timeout=15)
    res.raise_for_status()
    problems = res.json()["stat_status_pairs"]

    _CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
    _CACHE_PATH.write_text(json.dumps({"fetched_at": time.time(), "problems": problems}))
    return problems


def _get_slug(number: int) -> str:
    for p in _load_problems():
        if p["stat"]["frontend_question_id"] == number:
            return p["stat"]["question__title_slug"]
    raise typer.BadParameter(f"Problem {number} not found")


_PROBLEMS_PY = Path(__file__).parent / "problems.py"


def _solved_numbers() -> set[int]:
    tree = ast.parse(_PROBLEMS_PY.read_text())
    solved = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.FunctionDef):
            m = re.fullmatch(r"p(\d+).*", node.name)
            if m:
                solved.add(int(m.group(1)))
    return solved


def _next_unsolved() -> int:
    all_ids = {p["stat"]["frontend_question_id"] for p in _load_problems()}
    solved = _solved_numbers()
    unsolved = sorted(all_ids - solved)
    if not unsolved:
        raise typer.Exit("All problems solved. Impressive.")
    return unsolved[0]


def _get_question_detail(title_slug: str) -> dict:
    query = """
    query getQuestionDetail($titleSlug: String!) {
      question(titleSlug: $titleSlug) {
        questionFrontendId
        title
        difficulty
        content
        topicTags { name }
        stats
        sampleTestCase
        codeDefinition
      }
    }
    """
    res = requests.post(
        _GRAPHQL_URL,
        json={"operationName": "getQuestionDetail", "variables": {"titleSlug": title_slug}, "query": query},
        headers=_HEADERS,
        timeout=10,
    )
    res.raise_for_status()
    return res.json()["data"]["question"]


def _print_question(q: dict, slug: str | None = None):
    stats = json.loads(q["stats"])
    tags = ", ".join(t["name"] for t in q["topicTags"])
    code_defs = json.loads(q["codeDefinition"])
    languages = ", ".join(d["value"] for d in code_defs)

    typer.echo(f"[{q['questionFrontendId']}] {q['title']}  ({q['difficulty']})")
    if slug:
        typer.echo(f"URL: {_BASE_URL}/problems/{slug}/")
    typer.echo(f"Tags: {tags}")
    typer.echo(f"Accepted: {stats['totalAcceptedRaw']:,}  |  Submissions: {stats['totalSubmissionRaw']:,}  |  Rate: {stats['acRate']}")
    typer.echo(f"Languages: {languages}")
    typer.echo(f"\nSample test case:\n  {q['sampleTestCase']}")
    typer.echo(f"\n{'─' * 60}\n")
    typer.echo(_strip_html(q["content"]))


@app.command()
def get(number: Annotated[Optional[int], typer.Argument()] = None):
    """Fetch a LeetCode problem. Omit number to get the smallest unsolved problem."""
    n = number if number is not None else _next_unsolved()
    slug = _get_slug(n)
    _print_question(_get_question_detail(slug), slug)


@app.command()
def daily():
    """Fetch and display today's daily challenge."""
    query = """
    query getDailyChallenge {
      activeDailyCodingChallengeQuestion {
        question {
          questionFrontendId
          title
          titleSlug
          difficulty
          content
          topicTags { name }
          stats
          sampleTestCase
          codeDefinition
        }
      }
    }
    """
    res = requests.post(
        _GRAPHQL_URL,
        json={"operationName": "getDailyChallenge", "variables": {}, "query": query},
        headers=_HEADERS,
        timeout=10,
    )
    res.raise_for_status()
    q = res.json()["data"]["activeDailyCodingChallengeQuestion"]["question"]
    _print_question(q, q["titleSlug"])


if __name__ == "__main__":
    app()

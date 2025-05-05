from typing import List

with open("wordle_words.txt") as f:
    source_words = [x.strip('"') for x in f.read().split(",")]


def filter_words_pattern(pattern: str) -> List[int]: ...

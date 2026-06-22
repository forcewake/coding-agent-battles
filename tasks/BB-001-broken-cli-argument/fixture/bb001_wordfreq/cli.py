import argparse
import re
from collections import Counter
from pathlib import Path

WORD_RE = re.compile(r"[A-Za-z]+")


def count_words(text: str, min_length: int = 0) -> Counter[str]:
    words = [word.lower() for word in WORD_RE.findall(text)]
    if min_length:
        words = [word for word in words if len(word) >= min_length]
    return Counter(words)


def format_counts(counts: Counter[str]) -> str:
    lines = [f"{word}\t{count}" for word, count in sorted(counts.items(), key=lambda item: (-item[1], item[0]))]
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="wordfreq")
    parser.add_argument("path", help="Text file to analyze")
    parser.add_argument(
        "--min-length",
        action="store_true",
        default=0,
        help="Only include words with at least this many characters",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    text = Path(args.path).read_text(encoding="utf-8")
    output = format_counts(count_words(text, min_length=args.min_length))
    if output:
        print(output)
    return 0

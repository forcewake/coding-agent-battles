from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Iterable, NamedTuple


class Request(NamedTuple):
    method: str
    path: str
    status: int
    latency_ms: int


def parse_line(line: str) -> Request | None:
    parts = line.strip().split()
    if len(parts) != 5:
        return None
    _, method, path, status_text, latency_text = parts
    try:
        status = int(status_text)
        latency_ms = int(latency_text.removesuffix("ms"))
    except ValueError:
        return None
    return Request(method=method, path=path, status=status, latency_ms=latency_ms)


def parse_requests(lines: Iterable[str]) -> list[Request]:
    return [req for line in lines if (req := parse_line(line)) is not None]


def summarize(requests: list[Request]) -> dict[str, object]:
    status_counts = Counter(str(req.status) for req in requests)
    path_counts = Counter(req.path for req in requests)
    top_paths = sorted(path_counts.items(), key=lambda item: (-item[1], item[0]))
    return {
        "total_requests": len(requests),
        "status_counts": dict(sorted(status_counts.items())),
        "top_paths": [{"path": path, "count": count} for path, count in top_paths],
    }


def render_text(summary: dict[str, object]) -> str:
    lines = [f"total_requests	{summary['total_requests']}", "status_counts"]
    for status, count in summary["status_counts"].items():
        lines.append(f"{status}	{count}")
    lines.append("top_paths")
    for item in summary["top_paths"]:
        lines.append(f"{item['path']}	{item['count']}")
    return "\n".join(lines)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Summarize a tiny access log")
    parser.add_argument("logfile", type=Path, help="Path to access log")
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    requests = parse_requests(args.logfile.read_text(encoding="utf-8").splitlines())
    summary = summarize(requests)
    if args.json:
        print(json.dumps(summary))
    else:
        print(render_text(summary))
    return 0

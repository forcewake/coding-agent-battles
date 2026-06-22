from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SAMPLE = ROOT / "sample.log"


def run_cli(*args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "bb003_logstats", *args],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def test_default_text_output_is_preserved() -> None:
    result = run_cli(str(SAMPLE))
    assert result.returncode == 0, result.stderr
    assert result.stdout.strip().splitlines() == [
        "total_requests	7",
        "status_counts",
        "200	4",
        "404	2",
        "500	1",
        "top_paths",
        "/	3",
        "/api/items	2",
        "/login	1",
        "/missing	1",
    ]


def test_json_export_is_machine_readable_and_stable() -> None:
    result = run_cli("--json", str(SAMPLE))
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    assert payload == {
        "total_requests": 7,
        "status_counts": {"200": 4, "404": 2, "500": 1},
        "top_paths": [
            {"path": "/", "count": 3},
            {"path": "/api/items", "count": 2},
            {"path": "/login", "count": 1},
            {"path": "/missing", "count": 1},
        ],
    }

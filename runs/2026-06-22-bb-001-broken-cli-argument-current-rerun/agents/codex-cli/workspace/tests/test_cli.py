import subprocess
import sys
from pathlib import Path


def run_cli(*args: str, cwd: Path | None = None) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, "-m", "bb001_wordfreq", *args],
        cwd=cwd,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )


def test_default_counts_all_words(tmp_path: Path) -> None:
    sample = tmp_path / "sample.txt"
    sample.write_text("alpha beta beta cat dog elephant elephant fox\n", encoding="utf-8")

    result = run_cli(str(sample))

    assert result.returncode == 0, result.stderr
    assert result.stdout.splitlines() == [
        "beta\t2",
        "elephant\t2",
        "alpha\t1",
        "cat\t1",
        "dog\t1",
        "fox\t1",
    ]


def test_min_length_filters_short_words(tmp_path: Path) -> None:
    sample = tmp_path / "sample.txt"
    sample.write_text("alpha beta beta cat dog elephant elephant fox\n", encoding="utf-8")

    result = run_cli("--min-length", "4", str(sample))

    assert result.returncode == 0, result.stderr
    assert result.stdout.splitlines() == [
        "beta\t2",
        "elephant\t2",
        "alpha\t1",
    ]

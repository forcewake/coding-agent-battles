#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys


def run(cmd: list[str]) -> int:
    print("$", " ".join(cmd), flush=True)
    proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    print(proc.stdout, end="")
    return proc.returncode


def main() -> int:
    checks = [
        [sys.executable, "-m", "pytest", "-q"],
        [sys.executable, "-m", "bb001_wordfreq", "--min-length", "4", "sample.txt"],
        [sys.executable, "-m", "bb001_wordfreq", "sample.txt"],
    ]
    for cmd in checks:
        code = run(cmd)
        if code != 0:
            return code
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

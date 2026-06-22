#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
import sys


def run(cmd: list[str]) -> subprocess.CompletedProcess[str]:
    print("$", " ".join(cmd), flush=True)
    proc = subprocess.run(cmd, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, check=False)
    print(proc.stdout, end="")
    return proc


def main() -> int:
    for cmd in ([sys.executable, "-m", "pytest", "-q"], [sys.executable, "-m", "bb003_logstats", "sample.log"]):
        proc = run(cmd)
        if proc.returncode != 0:
            return proc.returncode
    proc = run([sys.executable, "-m", "bb003_logstats", "--json", "sample.log"])
    if proc.returncode != 0:
        return proc.returncode
    try:
        payload = json.loads(proc.stdout.split("\n", 1)[-1] if proc.stdout.startswith("$") else proc.stdout)
    except Exception:
        # The command output is printed above for diagnostics; run pytest already asserts exact shape.
        return 1
    if payload.get("total_requests") != 7:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

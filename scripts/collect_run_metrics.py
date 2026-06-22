#!/usr/bin/env python3
"""Collect stable, repo-local metrics from a coding-agent battle run.

This script intentionally reads only artifacts committed under a run directory.
Provider-specific token/cost extraction from local home directories should be done
by the controller and saved into `metrics.json`; those sources may contain secrets
or unrelated private sessions and are not safe to query from a public clone.
"""

from __future__ import annotations

import argparse
import json
import re
from pathlib import Path


def parse_meta(path: Path) -> dict[str, str]:
    data: dict[str, str] = {}
    if not path.exists():
        return data
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        if "=" in line:
            key, value = line.split("=", 1)
            data[key.strip()] = value.strip()
    return data


def count_changed_files(status_text: str) -> int:
    return sum(1 for line in status_text.splitlines() if line.strip())


def parse_verify(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8", errors="replace") if path.exists() else ""
    exit_match = re.search(r"\[verify_exit_code\]\s+(\d+)", text)
    wall_match = re.search(r"\[verify_wall_seconds\]\s+([0-9.]+)", text)
    return {
        "exit_code": int(exit_match.group(1)) if exit_match else None,
        "wall_seconds": float(wall_match.group(1)) if wall_match else None,
        "pytest_passed": bool(re.search(r"\b\d+ passed", text)),
        "cli_smoke_output_present": "beta\t2" in text and "alpha\t1" in text,
    }


def agent_artifact_metrics(agent_dir: Path) -> dict[str, object]:
    meta = parse_meta(agent_dir / "agent-meta.txt")
    status_text = (agent_dir / "git-status.txt").read_text(encoding="utf-8", errors="replace") if (agent_dir / "git-status.txt").exists() else ""
    diff_text = (agent_dir / "diff.patch").read_text(encoding="utf-8", errors="replace") if (agent_dir / "diff.patch").exists() else ""
    log_text = (agent_dir / "agent.log").read_text(encoding="utf-8", errors="replace") if (agent_dir / "agent.log").exists() else ""
    return {
        "agent": agent_dir.name,
        "exit_code": int(meta["exit_code"]) if meta.get("exit_code", "").isdigit() else None,
        "timed_out": meta.get("timed_out") == "True",
        "wall_seconds": float(meta["wall_seconds"]) if meta.get("wall_seconds") else None,
        "changed_files": count_changed_files(status_text),
        "diff_added_lines": sum(1 for line in diff_text.splitlines() if line.startswith("+") and not line.startswith("+++")),
        "diff_deleted_lines": sum(1 for line in diff_text.splitlines() if line.startswith("-") and not line.startswith("---")),
        "agent_log_indicates_pytest": "pytest" in log_text,
        "agent_log_indicates_red": "FAILED" in log_text or "1 failed" in log_text or "failed with exit code: 1" in log_text,
        "agent_log_indicates_cli_smoke": "python -m bb001_wordfreq" in log_text,
        "verify": parse_verify(agent_dir / "verify.log"),
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("run_dir", type=Path)
    args = parser.parse_args()
    run_dir = args.run_dir
    agents_dir = run_dir / "agents"
    metrics = {
        "run_dir": str(run_dir),
        "agents": [agent_artifact_metrics(p) for p in sorted(agents_dir.iterdir()) if p.is_dir()],
    }
    print(json.dumps(metrics, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

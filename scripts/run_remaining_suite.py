#!/usr/bin/env python3
from __future__ import annotations

import concurrent.futures as cf
import json
import os
import shlex
import shutil
import subprocess
import sys
import textwrap
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-06-22"
PI_BIN = os.environ.get("PI_BIN", "/home/forcewake/.nvm/versions/node/v24.15.0/bin/pi")
AGENT_IDS = ["mimo", "opencode", "agy", "claude-code", "codex-cli", "pi"]
TASK_DIRS = [
    ROOT / "tasks/BB-002-csv-edge-case-parser",
    ROOT / "tasks/BB-004-markdown-table-normalizer",
    ROOT / "tasks/BB-005-fastapi-auth-middleware-bug",
    ROOT / "tasks/BB-006-react-filter-search-ui",
    ROOT / "tasks/BB-007-sqlite-migration-rollback",
    ROOT / "tasks/BB-008-monorepo-dependency-upgrade",
    ROOT / "tasks/BB-009-observability-instrumentation",
    ROOT / "tasks/BB-010-docx-extraction-quality-fix",
    ROOT / "tasks/BB-011-greenfield-mini-product",
    ROOT / "tasks/BB-012-unknown-repo-leverage-task",
]


def run(cmd, cwd=None, input=None, timeout=None):
    return subprocess.run(
        cmd,
        cwd=cwd,
        input=input,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        timeout=timeout,
        check=False,
    )


def run_id(task: Path) -> str:
    return f"{DATE}-{task.name.lower()}"


def prompt_for(task: Path) -> str:
    task_md = (task / "task.md").read_text(encoding="utf-8")
    return f"""
You are fixing a benchmark fixture in an isolated git workspace.

{task_md}

Rules:
- Work only in the current workspace.
- Do not use network unless package installation is already required by verify.py.
- Run `python verify.py` before finishing.
- Keep the patch minimal and focused on the requested behavior.
- Do not edit tests unless the production code cannot reasonably satisfy them; if you edit tests, explain why in your final output.
- Do not print secrets or local credentials.

Expected final state: `python verify.py` exits 0.
""".strip()


def prepare() -> None:
    for task in TASK_DIRS:
        rid = run_id(task)
        rr = ROOT / "runs" / rid
        ev = rr / "evidence"
        ev.mkdir(parents=True, exist_ok=True)
        shutil.copy2(task / "task.md", rr / "task.md")
        if (task / "baseline-failure.log").exists():
            shutil.copy2(task / "baseline-failure.log", ev / "baseline-failure.log")
        (ev / "prompt.txt").write_text(prompt_for(task), encoding="utf-8")
        for agent in AGENT_IDS:
            ws = rr / "agents" / agent / "workspace"
            if ws.exists():
                shutil.rmtree(ws)
            shutil.copytree(task / "fixture", ws, ignore=shutil.ignore_patterns(".venv", "__pycache__", ".pytest_cache", "*.egg-info", "node_modules", ".git"))
            run(["git", "init", "-q"], cwd=ws)
            run(["git", "config", "user.email", "bench@example.invalid"], cwd=ws)
            run(["git", "config", "user.name", "Benchmark Baseline"], cwd=ws)
            run(["git", "add", "."], cwd=ws)
            run(["git", "commit", "-q", "-m", "baseline broken fixture"], cwd=ws)
    print(f"prepared {len(TASK_DIRS)} tasks x {len(AGENT_IDS)} agents")


def command_for(agent: str, ws: Path, prompt: str, agent_dir: Path):
    if agent == "mimo":
        return ["mimo", "run", "--dir", str(ws), "--dangerously-skip-permissions", prompt], None
    if agent == "opencode":
        return ["opencode", "run", "--dir", str(ws), "--dangerously-skip-permissions", prompt], None
    if agent == "agy":
        return [
            "agy",
            "--prompt", prompt,
            "--model", "Gemini 3.5 Flash (Medium)",
            "--dangerously-skip-permissions",
            "--print-timeout", "15m",
            "--log-file", str(agent_dir / "agy-cli.log"),
        ], None
    if agent == "claude-code":
        return [
            "claude", "--print", "--output-format", "json", "--dangerously-skip-permissions",
            "--no-session-persistence", "--max-budget-usd", "3.00", prompt,
        ], None
    if agent == "codex-cli":
        return [
            "codex", "exec", "-C", str(ws), "--sandbox", "danger-full-access",
            "--dangerously-bypass-approvals-and-sandbox", "--skip-git-repo-check", "-",
        ], prompt
    if agent == "pi":
        return [
            PI_BIN, "--provider", "zai-coding-cn", "--model", "glm-5.2", "--thinking", "xhigh",
            "--mode", "json", "--no-context-files", "--approve", "--tools", "read,write,edit,bash,grep,find,ls", "-p", prompt,
        ], None
    raise ValueError(agent)


def redact_cmd(cmd: list[str], prompt: str, stdin_prompt: str | None) -> str:
    out=[]
    for p in cmd:
        out.append("<PROMPT>" if p == prompt else shlex.quote(str(p)))
    if stdin_prompt is not None:
        out.append("<PROMPT_STDIN>")
    return " ".join(out)


def clean_workspace(ws: Path) -> None:
    for pat in [".venv", ".pytest_cache", "__pycache__", "*.egg-info", "node_modules", ".ruff_cache"]:
        for p in ws.rglob(pat) if "*" in pat else [ws / pat]:
            if p.exists():
                if p.is_dir(): shutil.rmtree(p, ignore_errors=True)
                else: p.unlink(missing_ok=True)


def run_one(task: Path, agent: str) -> dict:
    rid = run_id(task)
    rr = ROOT / "runs" / rid
    agent_dir = rr / "agents" / agent
    ws = agent_dir / "workspace"
    prompt = (rr / "evidence" / "prompt.txt").read_text(encoding="utf-8")
    cmd, stdin_prompt = command_for(agent, ws, prompt, agent_dir)
    agent_dir.mkdir(parents=True, exist_ok=True)
    started = time.time()
    try:
        proc = run(cmd, cwd=ws, input=stdin_prompt, timeout=1200)
        output = proc.stdout
        exit_code = proc.returncode
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        partial = exc.stdout or ""
        if isinstance(partial, bytes):
            partial = partial.decode("utf-8", "replace")
        output = partial + "\n[TIMEOUT] agent exceeded 1200 seconds\n"
        exit_code = 124
        timed_out = True
    wall = time.time() - started
    (agent_dir / "agent.log").write_text(output, encoding="utf-8", errors="replace")
    if agent == "claude-code":
        (agent_dir / "agent-output.json").write_text(output, encoding="utf-8", errors="replace")
    if agent == "pi":
        (agent_dir / "agent-output.jsonl").write_text(output, encoding="utf-8", errors="replace")
    (agent_dir / "agent-meta.txt").write_text(
        f"agent={agent}\nrun_id={rid}\nworkspace={ws}\nexit_code={exit_code}\ntimed_out={timed_out}\nwall_seconds={wall:.3f}\ncommand={redact_cmd(cmd, prompt, stdin_prompt)}\n",
        encoding="utf-8",
    )
    # Always collect diff/status even if agent failed.
    diff = run(["git", "diff", "--", "."], cwd=ws, timeout=60)
    (agent_dir / "diff.patch").write_text(diff.stdout, encoding="utf-8", errors="replace")
    status = run(["git", "status", "--short"], cwd=ws, timeout=60)
    (agent_dir / "git-status.txt").write_text(status.stdout, encoding="utf-8", errors="replace")
    # Independent verification.
    clean_workspace(ws)
    verify = run(["python", "verify.py"], cwd=ws, timeout=300)
    (agent_dir / "verify.log").write_text(verify.stdout, encoding="utf-8", errors="replace")
    verdict = "PASS" if verify.returncode == 0 else "FAIL"
    # Clean bulky transient files after verification but preserve workspace source/diff/logs.
    clean_workspace(ws)
    result = {
        "runId": rid,
        "task": task.name,
        "agent": agent,
        "agentExit": exit_code,
        "agentTimedOut": timed_out,
        "wall": round(wall, 3),
        "verifyExit": verify.returncode,
        "verdict": verdict,
    }
    (agent_dir / "result.json").write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(result), flush=True)
    return result


def run_all(max_workers: int = 6) -> None:
    pairs=[(task, agent) for task in TASK_DIRS for agent in AGENT_IDS]
    results=[]
    with cf.ThreadPoolExecutor(max_workers=max_workers) as ex:
        futs=[ex.submit(run_one, task, agent) for task, agent in pairs]
        for fut in cf.as_completed(futs):
            try:
                results.append(fut.result())
            except Exception as exc:
                err={"error": type(exc).__name__, "detail": str(exc)}
                results.append(err)
                print(json.dumps(err), flush=True)
    summary = {
        "tasks": len(TASK_DIRS),
        "agents": len(AGENT_IDS),
        "runs": len(results),
        "passes": sum(1 for r in results if r.get("verdict") == "PASS"),
        "fails": sum(1 for r in results if r.get("verdict") == "FAIL"),
        "errors": sum(1 for r in results if "error" in r),
        "results": results,
    }
    out = ROOT / "runs" / f"{DATE}-all-remaining-suite-summary.json"
    out.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    print("SUMMARY", json.dumps({k:v for k,v in summary.items() if k != 'results'}), flush=True)


def main() -> int:
    if len(sys.argv) < 2 or sys.argv[1] not in {"prepare", "run", "prepare-run"}:
        print("usage: run_remaining_suite.py prepare|run|prepare-run [max_workers]", file=sys.stderr)
        return 2
    if sys.argv[1] in {"prepare", "prepare-run"}:
        prepare()
    if sys.argv[1] in {"run", "prepare-run"}:
        max_workers = int(sys.argv[2]) if len(sys.argv) > 2 else 6
        run_all(max_workers=max_workers)
    return 0

if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shlex
import subprocess
import sys
import threading
import time
from pathlib import Path

RUN_ROOT = Path(__file__).resolve().parents[1]
PROMPT = (RUN_ROOT / "evidence" / "prompt.txt").read_text(encoding="utf-8")
PI_BIN = os.environ.get("PI_BIN", "/home/forcewake/.nvm/versions/node/v24.15.0/bin/pi")
TOKSCALE = ["npx", "--yes", "tokscale@latest"]

AGENTS = {
    "mimo": {
        "workspace": RUN_ROOT / "agents" / "mimo" / "workspace",
        "cmd": lambda ws: ["mimo", "run", "--dir", str(ws), "--dangerously-skip-permissions", PROMPT],
    },
    "opencode": {
        "workspace": RUN_ROOT / "agents" / "opencode" / "workspace",
        "cmd": lambda ws: ["opencode", "run", "--dir", str(ws), "--dangerously-skip-permissions", PROMPT],
    },
    "agy": {
        "workspace": RUN_ROOT / "agents" / "agy" / "workspace",
        "cmd": lambda ws: [
            "agy",
            "--print",
            "--dangerously-skip-permissions",
            "--print-timeout",
            "10m",
            "--log-file",
            str(RUN_ROOT / "agents" / "agy" / "agy-cli.log"),
            PROMPT,
        ],
        "tokscale_antigravity_sync": True,
    },
    "claude-code": {
        "workspace": RUN_ROOT / "agents" / "claude-code" / "workspace",
        "cmd": lambda ws: [
            "claude",
            "--print",
            "--output-format",
            "json",
            "--dangerously-skip-permissions",
            "--no-session-persistence",
            "--max-budget-usd",
            "1.00",
            PROMPT,
        ],
        "json_output": True,
    },
    "codex-cli": {
        "workspace": RUN_ROOT / "agents" / "codex-cli" / "workspace",
        "cmd": lambda ws: [
            "codex",
            "exec",
            "-C",
            str(ws),
            "--sandbox",
            "danger-full-access",
            "--dangerously-bypass-approvals-and-sandbox",
            "--skip-git-repo-check",
            "-",
        ],
        "stdin": True,
    },
    "pi": {
        "workspace": RUN_ROOT / "agents" / "pi" / "workspace",
        "cmd": lambda ws: [
            PI_BIN,
            "--provider",
            "zai-coding-cn",
            "--model",
            "glm-5.2",
            "--thinking",
            "xhigh",
            "--mode",
            "json",
            "--no-context-files",
            "--approve",
            "--tools",
            "read,write,edit,bash,grep,find,ls",
            "-p",
            PROMPT,
        ],
        "jsonl_output": True,
    },
}


def redact_command(cmd: list[str], stdin: bool) -> str:
    rendered = []
    for part in cmd:
        rendered.append("<PROMPT>" if part == PROMPT else shlex.quote(part))
    if stdin:
        rendered = rendered[:-1] + ["<PROMPT_STDIN>"]
    return " ".join(rendered)


def run_antigravity_sync(stop: threading.Event, log_path: Path) -> None:
    with log_path.open("w", encoding="utf-8", errors="replace") as f:
        attempt = 0
        while not stop.is_set():
            attempt += 1
            f.write(f"\n[sync_attempt] {attempt} {time.time()}\n")
            f.flush()
            try:
                proc = subprocess.run(
                    TOKSCALE + ["antigravity", "sync"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    text=True,
                    timeout=45,
                    check=False,
                )
                f.write(proc.stdout)
                f.write(f"\n[sync_exit] {proc.returncode}\n")
            except Exception as exc:  # best effort telemetry sidecar only
                f.write(f"[sync_error] {type(exc).__name__}: {exc}\n")
            f.flush()
            stop.wait(15)


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in AGENTS:
        print(f"usage: {sys.argv[0]} <{'|'.join(AGENTS)}>", file=sys.stderr)
        return 2
    agent = sys.argv[1]
    spec = AGENTS[agent]
    ws = spec["workspace"]
    evidence = RUN_ROOT / "agents" / agent
    evidence.mkdir(parents=True, exist_ok=True)
    log_path = evidence / "agent.log"
    meta_path = evidence / "agent-meta.txt"
    cmd = spec["cmd"](ws)
    started = time.time()
    stop_sync = threading.Event()
    sync_thread = None
    if spec.get("tokscale_antigravity_sync"):
        sync_thread = threading.Thread(
            target=run_antigravity_sync,
            args=(stop_sync, evidence / "tokscale-antigravity-sync.log"),
            daemon=True,
        )
        sync_thread.start()
    try:
        proc = subprocess.run(
            cmd,
            cwd=ws,
            input=PROMPT if spec.get("stdin") else None,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            timeout=900,
            check=False,
        )
        output = proc.stdout
        code = proc.returncode
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        partial = exc.stdout or ""
        if isinstance(partial, bytes):
            partial = partial.decode("utf-8", errors="replace")
        output = partial + "\n[TIMEOUT] agent exceeded 900 seconds\n"
        code = 124
        timed_out = True
    finally:
        stop_sync.set()
        if sync_thread:
            sync_thread.join(timeout=60)
    elapsed = time.time() - started
    log_path.write_text(output, encoding="utf-8", errors="replace")
    if spec.get("json_output"):
        (evidence / "agent-output.json").write_text(output, encoding="utf-8", errors="replace")
    if spec.get("jsonl_output"):
        (evidence / "agent-output.jsonl").write_text(output, encoding="utf-8", errors="replace")
    meta_path.write_text(
        "agent={agent}\nworkspace={ws}\nexit_code={code}\ntimed_out={timed_out}\nwall_seconds={elapsed:.3f}\ncommand={cmd}\n".format(
            agent=agent,
            ws=ws,
            code=code,
            timed_out=timed_out,
            elapsed=elapsed,
            cmd=redact_command(cmd, bool(spec.get("stdin"))),
        ),
        encoding="utf-8",
    )
    print(f"{agent}: exit={code} wall={elapsed:.1f}s log={log_path}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())

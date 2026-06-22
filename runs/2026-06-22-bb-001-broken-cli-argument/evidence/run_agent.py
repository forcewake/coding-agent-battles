#!/usr/bin/env python3
from __future__ import annotations

import subprocess
import sys
import time
from pathlib import Path

RUN_ROOT = Path(__file__).resolve().parents[1]
PROMPT = (RUN_ROOT / "evidence" / "prompt.txt").read_text(encoding="utf-8")

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
        "cmd": lambda ws: ["agy", "--print", "--dangerously-skip-permissions", "--print-timeout", "10m", PROMPT],
    },
    "claude-code": {
        "workspace": RUN_ROOT / "agents" / "claude-code" / "workspace",
        "cmd": lambda ws: ["claude", "--print", "--dangerously-skip-permissions", "--no-session-persistence", PROMPT],
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
}


def main() -> int:
    if len(sys.argv) != 2 or sys.argv[1] not in AGENTS:
        print(f"usage: {sys.argv[0]} <{'|'.join(AGENTS)}>", file=sys.stderr)
        return 2
    agent = sys.argv[1]
    spec = AGENTS[agent]
    ws = spec["workspace"]
    evidence = RUN_ROOT / "agents" / agent
    log_path = evidence / "agent.log"
    meta_path = evidence / "agent-meta.txt"
    cmd = spec["cmd"](ws)
    started = time.time()
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
    elapsed = time.time() - started
    log_path.write_text(output, encoding="utf-8", errors="replace")
    meta_path.write_text(
        "agent={agent}\nworkspace={ws}\nexit_code={code}\ntimed_out={timed_out}\nwall_seconds={elapsed:.3f}\ncommand={cmd}\n".format(
            agent=agent,
            ws=ws,
            code=code,
            timed_out=timed_out,
            elapsed=elapsed,
            cmd=" ".join(cmd[:-1] + (["<PROMPT_STDIN>"] if spec.get("stdin") else [])),
        ),
        encoding="utf-8",
    )
    print(f"{agent}: exit={code} wall={elapsed:.1f}s log={log_path}")
    return code


if __name__ == "__main__":
    raise SystemExit(main())

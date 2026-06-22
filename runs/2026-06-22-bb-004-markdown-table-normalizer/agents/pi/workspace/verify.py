#!/usr/bin/env python3
from __future__ import annotations
import json, os, subprocess, sys, venv
from pathlib import Path
ROOT = Path(__file__).resolve().parent
VENV = ROOT / ".venv"
if not VENV.exists():
    venv.EnvBuilder(with_pip=True).create(VENV)
py = VENV / "bin" / "python"
def run(cmd, **kw):
    print("[run]", " ".join(map(str, cmd)), flush=True)
    return subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kw)
r = run([str(py), "-m", "pip", "install", "-q", "-e", ".", "pytest"])
print(r.stdout, end="")
if r.returncode: sys.exit(r.returncode)
r = run([str(py), "-m", "pytest", "-q"])
print(r.stdout, end="")
if r.returncode: sys.exit(r.returncode)

print("[verify_exit_code] 0")

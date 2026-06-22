#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
AGENT_ORDER = [
    ("opencode", "OpenCode", "OpenCode / GLM-5.2", "glm-5.2"),
    ("claude-code", "Claude", "Claude Code / GLM-5.2", "glm-5.2[1m]"),
    ("mimo", "MiMo", "MiMoCode / GLM-5.2", "glm-5.2"),
    ("pi", "Pi", "Pi Coding Agent / GLM-5.2", "glm-5.2"),
    ("codex-cli", "Codex", "Codex CLI / GPT-5.5", "gpt-5.5"),
    ("agy", "agy", "Antigravity agy / Gemini 3.5 Flash Medium", "Gemini 3.5 Flash Medium"),
]


def clamp(n: float, lo=0.0, hi=1.0) -> float:
    return max(lo, min(hi, n))


def norm_low_better(v: float | None, values: list[float]) -> float:
    if v is None or not values:
        return 0.0
    lo, hi = min(values), max(values)
    if hi <= lo:
        return 1.0
    return clamp((hi - v) / (hi - lo))


def compute_scenario_scores(s: dict) -> None:
    agents = s.get("agents", [])
    wall_values = [float(a["wall"]) for a in agents if isinstance(a.get("wall"), (int, float))]
    token_values = [float(a["tokens"]) for a in agents if isinstance(a.get("tokens"), (int, float))]
    for a in agents:
        verdict_pass = a.get("verdict") == "PASS"
        agent_exit_ok = a.get("agentExit") == 0
        verify_exit_ok = a.get("verifyExit") == 0
        tokens_known = isinstance(a.get("tokens"), (int, float))
        cost_known = isinstance(a.get("cost"), (int, float))
        speed_norm = norm_low_better(a.get("wall"), wall_values)
        token_norm = norm_low_better(a.get("tokens"), token_values) if tokens_known else 0.0

        components = {
            "correctness": 40 if verdict_pass else 0,
            "baseline_red": 15 if a.get("red") else 0,
            "smoke": 15 if a.get("smoke") else 0,
            "independent_verify": 15 if verify_exit_ok else 0,
            "agent_exit": 5 if agent_exit_ok else 0,
            "speed": round(10 * speed_norm, 2),
        }
        a["process"] = int(round(min(100, sum(components.values()))))
        a["processComponents"] = components
        a["processLabel"] = "execution-quality composite"

    known = [a for a in agents if isinstance(a.get("process"), (int, float))]
    s["processBest"] = max(known, key=lambda a: a["process"])["id"] if known else None


def fmt_tokens(v):
    return "n/a" if v is None else f"{int(v):,}"


def fmt_cost(v):
    return "n/a" if v is None else f"${float(v):.6f}"


def update_run_markdown(run_dir: Path, scenario: dict) -> None:
    metric_rows = []
    result_rows = []
    for a in scenario.get("agents", []):
        metric_rows.append(
            f"| {a['short']} | {a['verdict']} | {a['wall']:.3f}s | {fmt_tokens(a.get('tokens'))} | "
            f"{fmt_cost(a.get('cost'))} | {a.get('patch', 'n/a')} | {a.get('process', 'n/a')} | "
            f"{a.get('processLabel', 'execution-quality composite')} |"
        )
        result_rows.append(
            f"| {a['short']} | {a['verdict']} | {a['wall']:.3f}s | {a.get('agentExit', 'n/a')} | "
            f"{a.get('verifyExit', 'n/a')} | {a.get('patch', 'n/a')} | {a.get('process', 'n/a')} |"
        )
    metrics_md = f"""# {scenario['id']} — {scenario['name']} metrics

## Scope

- Type: {scenario['type']}
- Difficulty: {scenario['difficulty']}
- Pass count: {scenario['passCount']}/{scenario['agentCount']}
- Execution score: deterministic composite from correctness, red-baseline capture, smoke evidence, independent verification, clean agent exit, and scenario-local speed percentile. Token/cost telemetry is reported separately and is not part of execution quality.

## Agent metrics

| Agent | Verdict | Wall | Tokens | Normalized public cost | Patch | Execution score | Notes |
|---|---:|---:|---:|---:|---:|---:|---|
""" + "\n".join(metric_rows) + "\n"
    results_md = f"""# {scenario['id']} — {scenario['name']} results

{scenario['summary']}

## Verification summary

| Agent | Verdict | Wall | Agent exit | Verify exit | Patch | Execution |
|---|---:|---:|---:|---:|---:|---:|
""" + "\n".join(result_rows) + """

## Evidence

Each agent has committed-style artifacts under `agents/<agent>/`:

- `agent.log`
- `agent-meta.txt`
- `diff.patch`
- `git-status.txt`
- `verify.log`
- `result.json`

Baseline failure is stored at `evidence/baseline-failure.log`.
"""
    (run_dir / "metrics.md").write_text(metrics_md, encoding="utf-8")
    (run_dir / "results.md").write_text(results_md, encoding="utf-8")


def main() -> None:
    data_path = ROOT / "docs/site-data.json"
    data = json.loads(data_path.read_text())
    for s in data.get("scenarios", []):
        compute_scenario_scores(s)
        if s.get("runId"):
            run_dir = ROOT / "runs" / s["runId"]
            docs_run_dir = ROOT / "docs" / "runs" / s["runId"]
            if run_dir.exists():
                (run_dir / "metrics.json").write_text(json.dumps(s, indent=2) + "\n", encoding="utf-8")
                update_run_markdown(run_dir, s)
            if docs_run_dir.exists():
                (docs_run_dir / "metrics.json").write_text(json.dumps(s, indent=2) + "\n", encoding="utf-8")
                if run_dir.exists():
                    (docs_run_dir / "metrics.md").write_text((run_dir / "metrics.md").read_text(), encoding="utf-8")
                    (docs_run_dir / "results.md").write_text((run_dir / "results.md").read_text(), encoding="utf-8")

    runs = [a for s in data.get("scenarios", []) for a in s.get("agents", [])]
    profiles = []
    for agent_id, short, label, model in AGENT_ORDER:
        ars = [a for a in runs if a.get("id") == agent_id]
        walls = [a.get("wall") for a in ars if isinstance(a.get("wall"), (int, float))]
        procs = [a.get("process") for a in ars if isinstance(a.get("process"), (int, float))]
        costs = [a.get("cost") for a in ars if isinstance(a.get("cost"), (int, float))]
        toks = [a.get("tokens") for a in ars if isinstance(a.get("tokens"), (int, float))]
        pcount = sum(1 for a in ars if a.get("verdict") == "PASS")
        profiles.append({
            "id": agent_id,
            "short": short,
            "label": label,
            "model": model,
            "runs": len(ars),
            "passes": pcount,
            "passRate": pcount / len(ars) if ars else 0,
            "avgWall": round(sum(walls) / len(walls), 3) if walls else None,
            "avgProcess": round(sum(procs) / len(procs), 1) if procs else None,
            "avgCost": round(sum(costs) / len(costs), 6) if costs else None,
            "totalTokens": sum(toks) if toks else None,
            "telemetryCoverage": len(costs) / len(ars) if ars else 0,
        })
    data["agentProfiles"] = profiles
    data.setdefault("scoreBasis", {})["executionQualityComposite"] = {
        "label": "Execution quality 0–100 composite",
        "formula": "40 correctness + 15 red-baseline + 15 smoke + 15 independent verify + 5 clean agent exit + 10 speed percentile",
        "notes": [
            "Speed is normalized within each scenario so scores are comparable inside a task, not across unrelated task sizes.",
            "Token/cost telemetry is intentionally excluded from execution quality; efficiency is shown separately in token and cost panels."
        ],
    }
    data_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    print("recomputed execution scores for", len(data.get("scenarios", [])), "scenarios")


if __name__ == "__main__":
    main()

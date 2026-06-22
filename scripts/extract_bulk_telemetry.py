#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sqlite3
import subprocess
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-06-22"
BULK_IDS = {"BB-002", "BB-004", "BB-005", "BB-006", "BB-007", "BB-008", "BB-009", "BB-010", "BB-011", "BB-012"}

ZAI_PRICING = {"input": 1.4, "cache": 0.26, "output": 4.4}
GPT55_PRICING = {"input": 5.0, "cache": 0.5, "output": 30.0}


def norm_cost_glm(input_tokens=0, cache_read_tokens=0, output_tokens=0, reasoning_tokens=0):
    return round((
        input_tokens * ZAI_PRICING["input"]
        + cache_read_tokens * ZAI_PRICING["cache"]
        + (output_tokens + reasoning_tokens) * ZAI_PRICING["output"]
    ) / 1_000_000, 6)


def norm_cost_gpt55(input_tokens=0, cache_read_tokens=0, output_tokens=0, reasoning_tokens=0):
    return round((
        input_tokens * GPT55_PRICING["input"]
        + cache_read_tokens * GPT55_PRICING["cache"]
        + (output_tokens + reasoning_tokens) * GPT55_PRICING["output"]
    ) / 1_000_000, 6)


def scenario_id_from_run_id(run_id: str) -> str:
    m = re.search(r"bb-(\d{3})", run_id)
    if not m:
        raise ValueError(run_id)
    return f"BB-{m.group(1)}"


def load_ccusage(source: str):
    out = subprocess.check_output([
        "npx", "--yes", "ccusage@latest", source, "session", "--json", "--since", "2026-06-22", "--until", "2026-06-23"
    ], cwd=ROOT, text=True)
    return json.loads(out)["sessions"]


def load_result(run_dir: Path, agent: str):
    p = run_dir / "agents" / agent / "result.json"
    return json.loads(p.read_text()) if p.exists() else None


def build_codex_map():
    sessions = load_ccusage("codex")
    by_uuid = {}
    for s in sessions:
        m = re.search(r"(019e[0-9a-f-]+)$", s.get("sessionFile", "")) or re.search(r"(019e[0-9a-f-]+)$", s.get("sessionId", ""))
        if m:
            by_uuid[m.group(1)] = s
    out = {}
    for log in ROOT.glob(f"runs/{DATE}-bb-*/agents/codex-cli/agent.log"):
        txt = log.read_text(errors="ignore")
        m = re.search(r"session id:\s*([0-9a-f-]{36})", txt)
        if not m:
            continue
        sess = by_uuid.get(m.group(1))
        if sess:
            run_id = log.parents[2].name
            out[run_id] = sess
    return out


def build_pi_map():
    out = {}
    for s in load_ccusage("pi"):
        pp = s.get("projectPath", "")
        m = re.search(r"2026-06-22-bb-\d{3}[^-]*(?:-[^-]+)*?-agents-pi-workspace", pp)
        # Easier and safer: scan known run ids as substrings after slash-to-dash conversion.
        for run_dir in ROOT.glob(f"runs/{DATE}-bb-*"):
            needle = str(run_dir.relative_to(ROOT)).replace("/", "-") + "-agents-pi-workspace"
            if needle in pp:
                out[run_dir.name] = s
                break
    return out


def build_opencode_map():
    sessions = {s["sessionId"]: s for s in load_ccusage("opencode")}
    log_path = Path.home() / ".local/share/opencode/log/opencode.log"
    out = {}
    if not log_path.exists():
        return out
    for line in log_path.read_text(errors="ignore").splitlines():
        if "message=created" not in line or "coding-agent-battles-init/runs/2026-06-22-bb-" not in line:
            continue
        md = re.search(r"directory=(\S+/runs/(2026-06-22-bb-[^/]+)/agents/opencode/workspace)", line)
        ms = re.search(r"id=(ses_\S+)", line)
        if md and ms and ms.group(1) in sessions:
            out[md.group(2)] = sessions[ms.group(1)]
    return out


def build_mimo_map():
    db = Path.home() / ".local/share/mimocode/mimocode.db"
    out = {}
    if not db.exists():
        return out
    con = sqlite3.connect(str(db))
    for sid, directory in con.execute("select id,directory from session where directory like ?", (f"%coding-agent-battles-init/runs/{DATE}-bb-%/agents/mimo/workspace",)):
        m = re.search(r"/runs/(2026-06-22-bb-[^/]+)/agents/mimo/workspace", directory)
        if not m:
            continue
        totals = {"input": 0, "output": 0, "reasoning": 0, "cache_read": 0, "cache_write": 0, "total": 0, "vendor_cost": 0.0}
        for (data,) in con.execute("select data from message where session_id=?", (sid,)):
            obj = json.loads(data)
            toks = obj.get("tokens")
            if not toks:
                continue
            cache = toks.get("cache") or {}
            totals["input"] += int(toks.get("input") or 0)
            totals["output"] += int(toks.get("output") or 0)
            totals["reasoning"] += int(toks.get("reasoning") or 0)
            totals["cache_read"] += int(cache.get("read") or 0)
            totals["cache_write"] += int(cache.get("write") or 0)
            totals["total"] += int(toks.get("total") or 0)
            totals["vendor_cost"] += float(obj.get("cost") or 0)
        if totals["total"]:
            totals["sessionId"] = sid
            out[m.group(1)] = totals
    return out


def extract_claude(run_dir: Path):
    p = run_dir / "agents/claude-code/agent-output.json"
    if not p.exists():
        return None
    obj = json.loads(p.read_text())
    usage = obj.get("usage") or {}
    input_tokens = int(usage.get("input_tokens") or 0)
    cache_read = int(usage.get("cache_read_input_tokens") or 0)
    cache_creation = int(usage.get("cache_creation_input_tokens") or 0)
    output_tokens = int(usage.get("output_tokens") or 0)
    total = input_tokens + cache_read + cache_creation + output_tokens
    return {
        "tokens": total,
        "cost": norm_cost_glm(input_tokens=input_tokens, cache_read_tokens=cache_read, output_tokens=output_tokens),
        "vendorCost": round(float(obj.get("total_cost_usd") or 0), 6),
        "telemetry_strategy": "claude_json_usage_normalized_public_cost",
        "telemetry_source": "agents/claude-code/agent-output.json",
        "token_breakdown": {"input": input_tokens, "cache_read": cache_read, "cache_creation": cache_creation, "output": output_tokens, "reasoning": 0},
    }


def from_ccusage_glm(sess, source: str, strategy: str, use_total_cost: bool = True):
    input_tokens = int(sess.get("inputTokens") or 0)
    cache_read = int(sess.get("cacheReadTokens") or 0)
    output_tokens = int(sess.get("outputTokens") or 0)
    reasoning = int(sess.get("reasoningOutputTokens") or 0)
    total = int(sess.get("totalTokens") or (input_tokens + cache_read + output_tokens + reasoning))
    cc_cost = sess.get("costUSD", sess.get("totalCost"))
    normalized = norm_cost_glm(input_tokens=input_tokens, cache_read_tokens=cache_read, output_tokens=output_tokens, reasoning_tokens=reasoning)
    return {
        "tokens": total,
        "cost": round(float(cc_cost), 6) if (use_total_cost and cc_cost not in (None, 0, 0.0)) else normalized,
        "vendorCost": round(float(cc_cost), 6) if cc_cost is not None else None,
        "telemetry_strategy": strategy,
        "telemetry_source": source,
        "telemetry_session": sess.get("sessionId"),
        "token_breakdown": {"input": input_tokens, "cache_read": cache_read, "cache_creation": int(sess.get("cacheCreationTokens") or 0), "output": output_tokens, "reasoning": reasoning},
    }


def from_ccusage_codex(sess):
    input_tokens = int(sess.get("inputTokens") or 0)
    cache_read = int(sess.get("cacheReadTokens") or 0)
    cache_creation = int(sess.get("cacheCreationTokens") or 0)
    output_tokens = int(sess.get("outputTokens") or 0)
    reasoning = int(sess.get("reasoningOutputTokens") or 0)
    cc_cost = round(float(sess.get("costUSD") or 0), 6)
    return {
        "tokens": int(sess.get("totalTokens") or 0),
        "cost": norm_cost_gpt55(input_tokens=input_tokens, cache_read_tokens=cache_read, output_tokens=output_tokens, reasoning_tokens=reasoning),
        "vendorCost": cc_cost,
        "telemetry_strategy": "ccusage_codex_session_exact_log_session_id_normalized_public_cost",
        "telemetry_source": "ccusage codex session + agents/codex-cli/agent.log session id",
        "telemetry_session": sess.get("sessionId"),
        "token_breakdown": {"input": input_tokens, "cache_read": cache_read, "cache_creation": cache_creation, "output": output_tokens, "reasoning": reasoning},
    }


def from_mimo(t):
    return {
        "tokens": int(t["total"]),
        "cost": norm_cost_glm(input_tokens=t["input"], cache_read_tokens=t["cache_read"], output_tokens=t["output"], reasoning_tokens=t["reasoning"]),
        "vendorCost": round(float(t.get("vendor_cost") or 0), 6),
        "telemetry_strategy": "mimocode_sqlite_session_exact_directory_normalized_public_cost",
        "telemetry_source": "local MiMoCode SQLite store session.directory + message.tokens",
        "telemetry_session": t.get("sessionId"),
        "token_breakdown": {"input": t["input"], "cache_read": t["cache_read"], "cache_creation": t["cache_write"], "output": t["output"], "reasoning": t["reasoning"]},
    }


def apply_agent(agent: dict, telemetry: dict | None):
    if not telemetry:
        agent["tokens"] = None
        agent["cost"] = None
        agent["telemetry_strategy"] = "unavailable"
        return
    agent.update({k: telemetry[k] for k in ["tokens", "cost", "telemetry_strategy", "telemetry_source", "token_breakdown"] if k in telemetry})
    if telemetry.get("vendorCost") is not None:
        agent["vendorCost"] = telemetry["vendorCost"]
    if telemetry.get("telemetry_session"):
        agent["telemetry_session"] = telemetry["telemetry_session"]


def fmt_tokens(v):
    return "n/a" if v is None else f"{int(v):,}"


def fmt_cost(v):
    return "n/a" if v is None else f"${float(v):.6f}"


def update_run_markdown(run_dir: Path, scenario: dict):
    rows = []
    for a in scenario["agents"]:
        note = "Telemetry exact; independent verify passed" if a.get("tokens") is not None and a.get("verdict") == "PASS" else (
            "Telemetry exact; independent verify failed" if a.get("tokens") is not None else "Telemetry unavailable"
        )
        rows.append(f"| {a['short']} | {a['verdict']} | {a['wall']:.3f}s | {fmt_tokens(a.get('tokens'))} | {fmt_cost(a.get('cost'))} | {a.get('telemetry_strategy','n/a')} | {note} |")
    metrics_md = f"""# {scenario['id']} — {scenario['name']} metrics

## Scope

- Type: {scenario['type']}
- Difficulty: {scenario['difficulty']}
- Pass count: {scenario['passCount']}/{scenario['agentCount']}
- Token/cost extraction: ccusage-first where available, then direct CLI/SQLite fallback with exact per-run attribution.

## Agent metrics

| Agent | Verdict | Wall | Tokens | Normalized public cost | Telemetry source | Notes |
|---|---:|---:|---:|---:|---|---|
""" + "\n".join(rows) + "\n"
    (run_dir / "metrics.md").write_text(metrics_md, encoding="utf-8")


def main():
    data_path = ROOT / "docs/site-data.json"
    data = json.loads(data_path.read_text())
    codex = build_codex_map()
    pi = build_pi_map()
    opencode = build_opencode_map()
    mimo = build_mimo_map()

    updated = 0
    audit = []
    for s in data["scenarios"]:
        if s["id"] not in BULK_IDS:
            continue
        run_dir = ROOT / "runs" / s["runId"]
        for a in s["agents"]:
            tel = None
            aid = a["id"]
            if aid == "claude-code":
                tel = extract_claude(run_dir)
            elif aid == "codex-cli" and s["runId"] in codex:
                tel = from_ccusage_codex(codex[s["runId"]])
            elif aid == "opencode" and s["runId"] in opencode:
                tel = from_ccusage_glm(opencode[s["runId"]], "ccusage opencode session + opencode.log exact directory/session id", "ccusage_opencode_exact_directory_session")
            elif aid == "pi" and s["runId"] in pi:
                # ccusage reports plan/native totalCost=0; compute normalized public estimate from token breakdown.
                tel = from_ccusage_glm(pi[s["runId"]], "ccusage pi session exact projectPath", "ccusage_pi_exact_project_path_normalized_public_cost", use_total_cost=False)
            elif aid == "mimo" and s["runId"] in mimo:
                tel = from_mimo(mimo[s["runId"]])
            elif aid == "agy":
                tel = None
            apply_agent(a, tel)
            if tel:
                updated += 1
                audit.append({"scenario": s["id"], "agent": aid, "tokens": tel["tokens"], "cost": tel["cost"], "strategy": tel["telemetry_strategy"]})
        known_cost = [a for a in s["agents"] if a.get("cost") is not None]
        s["cheapest"] = min(known_cost, key=lambda a: a["cost"])["id"] if known_cost else None
        proc_best = max(s["agents"], key=lambda a: (a.get("process") or 0)) if s.get("agents") else None
        s["processBest"] = proc_best["id"] if proc_best else None
        (run_dir / "metrics.json").write_text(json.dumps(s, indent=2) + "\n", encoding="utf-8")
        update_run_markdown(run_dir, s)
        docs_run = ROOT / "docs" / "runs" / s["runId"]
        if docs_run.exists():
            (docs_run / "metrics.json").write_text(json.dumps(s, indent=2) + "\n", encoding="utf-8")
            (docs_run / "metrics.md").write_text((run_dir / "metrics.md").read_text(), encoding="utf-8")

    runs = [a for s in data["scenarios"] for a in s.get("agents", [])]
    passes = sum(1 for a in runs if a.get("verdict") == "PASS")
    known_cost = [a.get("cost") for a in runs if a.get("cost") is not None]
    data["kpis"] = {
        "scenarios": len(data["scenarios"]),
        "agentRuns": len(runs),
        "passes": passes,
        "passRate": passes / len(runs) if runs else 0,
        "normalizedPublicCost": round(sum(known_cost), 6),
        "costCoverage": len(known_cost) / len(runs) if runs else 0,
    }
    profiles = []
    agent_order = [("opencode", "OpenCode", "OpenCode / GLM-5.2", "glm-5.2"), ("claude-code", "Claude", "Claude Code / GLM-5.2", "glm-5.2[1m]"), ("mimo", "MiMo", "MiMoCode / GLM-5.2", "glm-5.2"), ("pi", "Pi", "Pi Coding Agent / GLM-5.2", "glm-5.2"), ("codex-cli", "Codex", "Codex CLI / GPT-5.5", "gpt-5.5"), ("agy", "agy", "Antigravity agy / Gemini 3.5 Flash Medium", "Gemini 3.5 Flash Medium")]
    for agent_id, short, label, model in agent_order:
        ars = [a for a in runs if a.get("id") == agent_id]
        walls = [a.get("wall") for a in ars if a.get("wall") is not None]
        procs = [a.get("process") for a in ars if a.get("process") is not None]
        costs = [a.get("cost") for a in ars if a.get("cost") is not None]
        toks = [a.get("tokens") for a in ars if a.get("tokens") is not None]
        pcount = sum(1 for a in ars if a.get("verdict") == "PASS")
        profiles.append({
            "id": agent_id, "short": short, "label": label, "model": model,
            "runs": len(ars), "passes": pcount, "passRate": pcount / len(ars) if ars else 0,
            "avgWall": round(sum(walls) / len(walls), 3) if walls else None,
            "avgProcess": round(sum(procs) / len(procs), 1) if procs else None,
            "avgCost": round(sum(costs) / len(costs), 6) if costs else None,
            "totalTokens": sum(toks) if toks else None,
            "telemetryCoverage": len(costs) / len(ars) if ars else 0,
        })
    data["agentProfiles"] = profiles
    data.setdefault("telemetryBasis", {})["bulkSuiteExtraction"] = {
        "date": "2026-06-22",
        "updatedAgentRuns": updated,
        "coverage": "50/60 bulk runs; agy remains unavailable",
        "sources": [
            "ccusage codex exact session id from agent.log; normalized public cost recomputed from input/cache/output/reasoning tokens, vendorCost preserves ccusage native cost",
            "ccusage opencode exact session id from opencode.log directory",
            "ccusage pi exact projectPath",
            "Claude Code agent-output.json usage",
            "MiMoCode SQLite exact session.directory + message.tokens",
        ],
    }
    if "pricingBasis" in data:
        lim = data["pricingBasis"].setdefault("limitations", [])
        stale = "Bulk BB-002/004-012 run currently reports verified wall-clock/pass-fail only; token/cost fields stay n/a until ccusage/fallback telemetry attribution is performed."
        data["pricingBasis"]["limitations"] = [x for x in lim if x != stale]
        msg = "Bulk BB-002/004-012 telemetry restored for Claude, Codex, OpenCode, MiMo, and Pi using exact per-run attribution; agy remains n/a because Antigravity transcripts still lack reliable token/cost export."
        if msg not in data["pricingBasis"]["limitations"]:
            data["pricingBasis"]["limitations"].append(msg)
    data_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")
    (ROOT / "runs" / "2026-06-22-all-remaining-suite-telemetry-audit.json").write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    docs_summary = ROOT / "docs" / "runs" / "2026-06-22-all-remaining-suite-telemetry-audit.json"
    docs_summary.write_text(json.dumps(audit, indent=2) + "\n", encoding="utf-8")
    print(f"restored telemetry for {updated} bulk agent runs")


if __name__ == "__main__":
    main()

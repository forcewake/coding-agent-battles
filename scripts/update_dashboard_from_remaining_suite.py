#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import subprocess
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATE = "2026-06-22"
AGENTS = [
    ("opencode", "OpenCode", "OpenCode / GLM-5.2", "glm-5.2"),
    ("claude-code", "Claude", "Claude Code / GLM-5.2", "glm-5.2[1m]"),
    ("mimo", "MiMo", "MiMoCode / GLM-5.2", "glm-5.2"),
    ("pi", "Pi", "Pi Coding Agent / GLM-5.2", "glm-5.2"),
    ("codex-cli", "Codex", "Codex CLI / GPT-5.5", "gpt-5.5"),
    ("agy", "agy", "Antigravity agy / Gemini 3.5 Flash Medium", "Gemini 3.5 Flash Medium"),
]
META = {
    "BB-001": ("Broken CLI argument", "CLI bugfix", "L0", "Fix wordfreq --min-length parsing while preserving default word count output."),
    "BB-002": ("CSV edge-case parser", "Library bugfix", "L0", "CSV parser edge cases: quoted commas, escaped quotes, blank rows, deterministic grouping."),
    "BB-003": ("JSON export for existing CLI", "CLI feature", "L1", "Feature addition: add stable JSON export while preserving text UX."),
    "BB-004": ("Markdown table normalizer", "Text processing", "L1", "Normalize Markdown pipe tables with padded columns and idempotent output."),
    "BB-005": ("FastAPI auth middleware bug", "Backend debugging", "L2", "Fix FastAPI auth dependency so admin is protected while health remains public."),
    "BB-006": ("React filter/search UI", "Frontend behavior", "L2", "Browser-visible search/filter state model with stable empty-state copy."),
    "BB-007": ("SQLite migration with rollback", "Data migration", "L2", "Safe SQLite upgrade/downgrade preserving rows and idempotent upgrade behavior."),
    "BB-008": ("Monorepo dependency upgrade", "Tooling / monorepo", "L3", "Adapt app package to upgraded shared slug API without reintroducing legacy export."),
    "BB-009": ("Observability instrumentation", "Non-functional backend", "L3", "Add safe structured request events with correlation IDs and no secret logging."),
    "BB-010": ("DOCX extraction quality fix", "Document extraction", "L3", "Improve OOXML/DOCX extraction to preserve paragraph/table order and XML entity decoding."),
    "BB-011": ("Greenfield mini-product", "Greenfield product", "L4", "Build a tiny FastAPI benchmark registry from tests/spec."),
    "BB-012": ("Unknown repo leverage task", "External helper leverage", "L4", "Use provided vendor text helper instead of reimplementing tokenization incorrectly."),
}

def slug_for_id(sid: str) -> str:
    return sid.lower()

def id_from_run(run_id: str) -> str:
    m = re.search(r"bb-(\d{3})", run_id)
    if not m: raise ValueError(run_id)
    return f"BB-{m.group(1)}"

def load_results():
    rows=[]
    for p in (ROOT/"runs").glob(f"{DATE}-bb-*/agents/*/result.json"):
        r=json.loads(p.read_text())
        sid=id_from_run(r["runId"])
        rows.append((sid,p,r))
    return rows

def write_run_reports(grouped):
    for sid, rows in grouped.items():
        name, typ, level, summary = META[sid]
        run_id = rows[0][2]["runId"]
        rr = ROOT/"runs"/run_id
        agent_entries=[]
        for agent_id, short, label, model in AGENTS:
            match = next((r for _,_,r in rows if r["agent"] == agent_id), None)
            if not match: continue
            passed = match["verdict"] == "PASS"
            agent_entries.append({
                "id": agent_id,
                "short": short,
                "label": label,
                "model": model,
                "verdict": match["verdict"],
                "wall": match["wall"],
                "tokens": None,
                "cost": None,
                "patch": 100 if passed else 0,
                "process": None,
                "processLabel": "execution-quality composite pending recompute",
                "red": True,
                "smoke": passed,
                "agentExit": match["agentExit"],
                "verifyExit": match["verifyExit"],
            })
        pass_count=sum(1 for a in agent_entries if a["verdict"]=="PASS")
        fastest=min((a for a in agent_entries if a["verdict"]=="PASS" and a["wall"] is not None), key=lambda a:a["wall"], default=None)
        proc_best=max(agent_entries, key=lambda a:(a["process"] or 0)) if agent_entries else None
        scenario={
            "id": sid,
            "name": name,
            "runId": run_id,
            "type": typ,
            "difficulty": level,
            "summary": summary,
            "passCount": pass_count,
            "agentCount": len(agent_entries),
            "fastest": fastest["id"] if fastest else None,
            "cheapest": None,
            "processBest": proc_best["id"] if proc_best else None,
            "agents": agent_entries,
            "links": {
                "results": f"runs/{run_id}/results.md",
                "metrics": f"runs/{run_id}/metrics.md",
                "json": f"runs/{run_id}/metrics.json",
            },
            "slug": slug_for_id(sid),
        }
        (rr/"metrics.json").write_text(json.dumps(scenario, indent=2)+"\n", encoding="utf-8")
        table="\n".join(
            f"| {a['short']} | {a['verdict']} | {a['wall']:.3f}s | {a['agentExit']} | {a['verifyExit']} | {a['patch']} | {a['process']} |"
            for a in agent_entries
        )
        md=f"""# {sid} — {name} results

{summary}

## Verification summary

| Agent | Verdict | Wall | Agent exit | Verify exit | Patch | Process |
|---|---:|---:|---:|---:|---:|---:|
{table}

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
        (rr/"results.md").write_text(md, encoding="utf-8")
        metrics_md=f"""# {sid} — {name} metrics

## Scope

- Type: {typ}
- Difficulty: {level}
- Pass count: {pass_count}/{len(agent_entries)}
- Token/cost extraction: not yet normalized for this bulk run; fields remain `n/a` until a separate ccusage/fallback telemetry pass.

## Agent metrics

| Agent | Verdict | Wall | Tokens | Cost | Notes |
|---|---:|---:|---:|---:|---|
"""
        for a in agent_entries:
            note="Hermes-independent verify passed" if a["verdict"]=="PASS" else "Agent exited but independent verify failed"
            metrics_md += f"| {a['short']} | {a['verdict']} | {a['wall']:.3f}s | n/a | n/a | {note} |\n"
        (rr/"metrics.md").write_text(metrics_md, encoding="utf-8")
    return [json.loads((ROOT/"runs"/rows[0][2]["runId"]/"metrics.json").read_text()) for sid, rows in sorted(grouped.items())]

def update_site_data(new_scenarios):
    path=ROOT/"docs/site-data.json"
    data=json.loads(path.read_text())
    # Preserve old scenarios by id, replace/add new.
    by_id={s["id"]:s for s in data["scenarios"]}
    for s in new_scenarios: by_id[s["id"]]=s
    order=["BB-001","BB-002","BB-003","BB-004","BB-005","BB-006","BB-007","BB-008","BB-009","BB-010","BB-011","BB-012"]
    data["scenarios"]=[by_id[i] for i in order if i in by_id]
    runs=[a for s in data["scenarios"] for a in s.get("agents",[])]
    passes=sum(1 for a in runs if a.get("verdict")=="PASS")
    cost_known=[a.get("cost") for a in runs if a.get("cost") is not None]
    data["kpis"]={
        "scenarios": len(data["scenarios"]),
        "agentRuns": len(runs),
        "passes": passes,
        "passRate": passes/len(runs) if runs else 0,
        "normalizedPublicCost": round(sum(cost_known), 6),
        "costCoverage": len(cost_known)/len(runs) if runs else 0,
    }
    # Recompute profiles in AGENTS order.
    profiles=[]
    for agent_id, short, label, model in AGENTS:
        ars=[a for a in runs if a.get("id")==agent_id]
        pass_count=sum(1 for a in ars if a.get("verdict")=="PASS")
        walls=[a.get("wall") for a in ars if a.get("wall") is not None]
        procs=[a.get("process") for a in ars if a.get("process") is not None]
        costs=[a.get("cost") for a in ars if a.get("cost") is not None]
        toks=[a.get("tokens") for a in ars if a.get("tokens") is not None]
        profiles.append({
            "id": agent_id,
            "short": short,
            "label": label,
            "model": model,
            "runs": len(ars),
            "passes": pass_count,
            "passRate": pass_count/len(ars) if ars else 0,
            "avgWall": round(sum(walls)/len(walls), 3) if walls else None,
            "avgProcess": round(sum(procs)/len(procs), 1) if procs else None,
            "avgCost": round(sum(costs)/len(costs), 6) if costs else None,
            "totalTokens": sum(toks) if toks else None,
            "telemetryCoverage": len(costs)/len(ars) if ars else 0,
        })
    data["agentProfiles"]=profiles
    if "pricingBasis" in data:
        lim=data["pricingBasis"].setdefault("limitations", [])
        msg="Bulk BB-002/004-012 run currently reports verified wall-clock/pass-fail only; token/cost fields stay n/a until ccusage/fallback telemetry attribution is performed."
        if msg not in lim: lim.append(msg)
    path.write_text(json.dumps(data, indent=2)+"\n", encoding="utf-8")

def write_scenario_pages(scenarios):
    tpl='''<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Scenario {sid} — Coding Agent Battles</title>
  <meta name="description" content="Scenario {sid} results for Coding Agent Battles." />
  <link rel="stylesheet" href="../styles.css?v=20260622-cleanreview-fixes" />
  <script src="../vendor/d3.v7.min.js"></script>
</head>
<body data-page="scenario" data-scenario-id="{slug}">
  <header class="site-header">
    <nav class="nav-shell" aria-label="Primary navigation">
      <a class="brand" href="../" aria-label="Coding Agent Battles home"><span class="brand-badge">CAB</span><span class="brand-name">Coding Agent Battles</span></a>
      <ul class="nav-links" role="list"><li><a href="../">Home</a></li><li><a href="../agents.html">Agents</a></li><li><a href="../#method">Method</a></li><li><a href="https://github.com/forcewake/coding-agent-battles" class="nav-gh" target="_blank" rel="noopener">GitHub ↗</a></li></ul>
    </nav>
  </header>
  <main>
    <section class="content-section" id="scenario-detail">
      <div class="section-header"><div><p class="label-overline">Scenario detail</p><h2 class="section-title" id="detail-title">Loading...</h2></div><p class="section-desc" id="detail-summary">—</p></div>
      <div id="scenario-panel" class="scenario-panel" style="margin-bottom:40px"></div>
      <div class="detail-grid"><div class="detail-chart-card wide"><p class="chart-label">Latency vs token burn</p><div id="frontierChart" role="img" aria-label="Scatter plot of wall-clock seconds versus token count"></div></div><div class="detail-bars-group"><div class="detail-chart-card"><p class="chart-label">Wall-clock <span class="chart-unit">seconds</span></p><div id="timeBars" class="bar-list"></div></div><div class="detail-chart-card"><p class="chart-label">Execution quality <span class="chart-unit">0–100 composite</span></p><div id="qualityBars" class="bar-list"></div></div><div class="detail-chart-card"><p class="chart-label">Normalized public cost <span class="chart-unit">USD estimate</span></p><div id="costBars" class="bar-list"></div></div></div></div>
      <details class="evidence-details" id="score-table-details" open><summary class="evidence-summary">Full metrics table</summary><div class="table-wrap"><table id="scoreTable" aria-label="Full metrics for scenario"><thead><tr><th>Agent</th><th>Wall (s)</th><th>Tokens</th><th>Cost</th><th>Patch %</th><th>Execution</th><th>Evidence</th></tr></thead><tbody></tbody></table></div></details>
    </section>
  </main>
  <footer class="site-footer"><span>Built from committed benchmark artifacts.</span><a href="https://github.com/forcewake/coding-agent-battles" target="_blank" rel="noopener">forcewake/coding-agent-battles ↗</a></footer>
  <script src="../app.js?v=20260622-cleanreview-fixes" type="module"></script>
</body>
</html>
'''
    out=ROOT/"docs/scenarios"
    out.mkdir(exist_ok=True)
    for s in scenarios:
        (out/f"{s['slug']}.html").write_text(tpl.format(sid=s["id"], slug=s["slug"]), encoding="utf-8")

def patch_home_copy():
    idx=ROOT/"docs/index.html"
    txt=idx.read_text()
    txt=txt.replace("Six agents.<br>Two scenarios.<br>All claims verified.", "Six agents.<br>Twelve scenarios.<br>Verified runs.")
    txt=txt.replace("Two scenarios are not a final leaderboard. BB-001 proves the harness (argparse bugfix), BB-003 adds a real feature task (JSON export). Together they establish the matrix shape and telemetry pipeline for future scenarios.", "The corpus now spans calibration bugs, text processing, backend/API fixes, UI logic, migrations, monorepo upgrades, observability, document extraction, greenfield product work, and external-helper leverage.")
    txt=txt.replace("Added BB-003 JSON-export task and fixture.", "Added the remaining BB-002 and BB-004–BB-012 tasks and fixtures.")
    txt=txt.replace("Promoted Pages from run detail to corpus dashboard.", "Promoted Pages to a multi-scenario benchmark briefing with per-scenario detail pages.")
    idx.write_text(txt)

rows=load_results()
remaining=[x for x in rows if x[0] in META]
grouped=defaultdict(list)
for sid,p,r in remaining: grouped[sid].append((sid,p,r))
assert set(grouped)==set(META), sorted(set(META)-set(grouped))
new=write_run_reports(grouped)
update_site_data(new)
write_scenario_pages(new)
patch_home_copy()
print('wrote reports and dashboard for', len(new), 'new scenarios')
telemetry_script = ROOT / "scripts" / "extract_bulk_telemetry.py"
if telemetry_script.exists():
    subprocess.run(["python", str(telemetry_script)], cwd=ROOT, check=True)
score_script = ROOT / "scripts" / "recompute_execution_scores.py"
if score_script.exists():
    subprocess.run(["python", str(score_script)], cwd=ROOT, check=True)

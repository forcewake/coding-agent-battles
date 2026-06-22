#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
import re
import subprocess
import sys
from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
RUNS = ROOT / "runs"
AUDIT_DIR = DOCS / "audit"
AGENT_ORDER = ["opencode", "claude-code", "mimo", "pi", "codex-cli", "agy"]
FLOAT_FIELDS = {"wall", "cost", "vendorCost"}
AGENT_FIELDS = [
    "id", "short", "label", "model", "verdict", "wall", "tokens", "cost", "patch", "process",
    "red", "smoke", "agentExit", "verifyExit", "telemetry_strategy", "telemetry_source",
    "vendorCost", "telemetry_session", "processLabel",
]

@dataclass
class Check:
    id: str
    status: str
    severity: str
    claim: str
    evidence: list[str]
    details: str = ""


def rel(p: Path | str) -> str:
    try:
        return str(Path(p).relative_to(ROOT))
    except Exception:
        return str(p)


def add(checks: list[Check], id: str, ok: bool, claim: str, evidence: list[Path | str], details: str = "", severity: str = "major") -> None:
    checks.append(Check(id=id, status="PASS" if ok else "FAIL", severity="info" if ok else severity, claim=claim, evidence=[rel(e) for e in evidence], details=details))


def warn(checks: list[Check], id: str, claim: str, evidence: list[Path | str], details: str = "", severity: str = "minor") -> None:
    checks.append(Check(id=id, status="WARN", severity=severity, claim=claim, evidence=[rel(e) for e in evidence], details=details))


def load_json(p: Path) -> Any:
    return json.loads(p.read_text(encoding="utf-8"))


def eq(a: Any, b: Any, field: str = "") -> bool:
    if field in FLOAT_FIELDS and a is not None and b is not None:
        return math.isclose(float(a), float(b), rel_tol=0, abs_tol=1e-6)
    return a == b


def parse_results_table(path: Path) -> dict[str, dict[str, str]]:
    rows: dict[str, dict[str, str]] = {}
    if not path.exists():
        return rows
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.startswith("|") or "---" in line or "Agent" in line:
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 7:
            rows[cells[0]] = {
                "verdict": cells[1],
                "wall": cells[2],
                "agentExit": cells[3],
                "verifyExit": cells[4],
                "patch": cells[5],
                "process": cells[6],
            }
    return rows


def expected_row(agent: dict[str, Any]) -> dict[str, str]:
    def cell(v: Any) -> str:
        return "n/a" if v is None else str(v)
    wall = agent.get("wall")
    wall_text = f"{float(wall):.3f}s" if wall is not None else "n/a"
    return {
        "verdict": str(agent.get("verdict")),
        "wall": wall_text,
        "agentExit": cell(agent.get("agentExit")),
        "verifyExit": cell(agent.get("verifyExit")),
        "patch": cell(agent.get("patch")),
        "process": cell(agent.get("process")),
    }


def run_chrome(url: str, out: Path) -> tuple[int, str]:
    chrome = None
    for cmd in ["google-chrome", "chromium", "chromium-browser"]:
        r = subprocess.run(["bash", "-lc", f"command -v {cmd}"], text=True, capture_output=True)
        if r.returncode == 0 and r.stdout.strip():
            chrome = r.stdout.strip()
            break
    if not chrome:
        return 99, "chrome not found"
    cmd = [chrome, "--headless", "--disable-gpu", "--no-sandbox", "--dump-dom", "--virtual-time-budget=9000", url]
    r = subprocess.run(cmd, text=True, capture_output=True, timeout=35)
    out.write_text(r.stdout, encoding="utf-8")
    return r.returncode, r.stderr[-4000:]


def audit(public: bool = False, base_url: str = "https://forcewake.github.io/coding-agent-battles") -> dict[str, Any]:
    checks: list[Check] = []
    site_path = DOCS / "site-data.json"
    data = load_json(site_path)
    scenarios = data.get("scenarios", [])
    all_agents = [a for s in scenarios for a in s.get("agents", [])]

    add(checks, "site.scenario_count", len(scenarios) == 12, "Dashboard claims 12 scenarios", [site_path], f"actual={len(scenarios)}", "blocker")
    add(checks, "site.agent_run_count", len(all_agents) == 72, "Dashboard claims 72 agent runs", [site_path], f"actual={len(all_agents)}", "blocker")
    pass_count = sum(1 for a in all_agents if a.get("verdict") == "PASS")
    add(checks, "site.pass_count", pass_count == data.get("kpis", {}).get("passes") == 70, "Pass count is 70 and matches KPI", [site_path], f"actual={pass_count}, kpi={data.get('kpis', {}).get('passes')}", "blocker")
    cost_known = sum(1 for a in all_agents if a.get("cost") is not None)
    add(checks, "site.cost_coverage", cost_known == 60, "Cost/token coverage is 60/72; agy remains n/a", [site_path], f"cost_known={cost_known}", "major")

    for s in scenarios:
        sid = s["id"]
        run_id = s.get("runId")
        docs_run = DOCS / "runs" / run_id
        raw_run = RUNS / run_id
        links = s.get("links", {})
        docs_metrics_path = DOCS / links.get("json", "")
        docs_results_path = DOCS / links.get("results", "")
        docs_metrics_md_path = DOCS / links.get("metrics", "")
        raw_metrics_path = raw_run / "metrics.json"
        raw_results_path = raw_run / "results.md"
        baseline_path = raw_run / "evidence" / "baseline-failure.log"

        add(checks, f"{sid}.docs_run_exists", docs_run.exists(), f"{sid} public docs/runs mirror exists", [docs_run], "", "blocker")
        add(checks, f"{sid}.raw_run_exists", raw_run.exists(), f"{sid} raw run directory exists", [raw_run], "", "blocker")
        for name, p in [("metrics.json", docs_metrics_path), ("metrics.md", docs_metrics_md_path), ("results.md", docs_results_path), ("raw metrics.json", raw_metrics_path), ("raw results.md", raw_results_path)]:
            add(checks, f"{sid}.{name}.exists", p.exists(), f"{sid} {name} exists", [p], "", "blocker")

        if docs_metrics_path.exists():
            dm = load_json(docs_metrics_path)
            add(checks, f"{sid}.metrics.scenario_fields", all(eq(s.get(k), dm.get(k), k) for k in ["id", "name", "runId", "type", "difficulty", "summary", "passCount", "agentCount", "fastest", "cheapest", "processBest"]), f"{sid} site-data scenario fields match docs metrics.json", [site_path, docs_metrics_path], "", "major")
            by_id = {a["id"]: a for a in dm.get("agents", [])}
            mismatches = []
            for a in s.get("agents", []):
                b = by_id.get(a["id"])
                if not b:
                    mismatches.append(f"missing {a['id']}")
                    continue
                for k in AGENT_FIELDS:
                    if k in a or k in b:
                        if not eq(a.get(k), b.get(k), k):
                            mismatches.append(f"{a['id']}.{k}: site={a.get(k)!r} metrics={b.get(k)!r}")
                if a.get("token_breakdown") != b.get("token_breakdown"):
                    mismatches.append(f"{a['id']}.token_breakdown differs")
                if a.get("processComponents") != b.get("processComponents"):
                    mismatches.append(f"{a['id']}.processComponents differs")
            add(checks, f"{sid}.site_vs_docs_metrics_agents", not mismatches, f"{sid} site-data agent rows match docs metrics.json", [site_path, docs_metrics_path], "; ".join(mismatches[:10]), "major")

        if raw_metrics_path.exists() and docs_metrics_path.exists():
            raw = load_json(raw_metrics_path)
            docs = load_json(docs_metrics_path)
            add(checks, f"{sid}.raw_vs_public_metrics", raw == docs, f"{sid} raw metrics.json equals public docs metrics.json", [raw_metrics_path, docs_metrics_path], "", "major")

        if docs_results_path.exists():
            rows = parse_results_table(docs_results_path)
            row_mismatches = []
            for a in s.get("agents", []):
                short = a.get("short")
                got = rows.get(short)
                exp = expected_row(a)
                if got != exp:
                    row_mismatches.append(f"{short}: expected={exp} got={got}")
            add(checks, f"{sid}.results_md_matches_site", not row_mismatches, f"{sid} results.md table matches site-data verdict/wall/exits/patch/execution", [docs_results_path, site_path], "; ".join(row_mismatches[:6]), "major")

        add(checks, f"{sid}.baseline_failure_log", baseline_path.exists() and baseline_path.stat().st_size > 0, f"{sid} red-baseline evidence exists", [baseline_path], "", "major")

        pass_wall_agents = [a for a in s["agents"] if a.get("wall") is not None and a.get("verdict") == "PASS"]
        expected_fastest = min(pass_wall_agents, key=lambda a: a["wall"])["id"] if pass_wall_agents else None
        add(checks, f"{sid}.fastest", s.get("fastest") == expected_fastest, f"{sid} fastest claim matches minimum wall-clock among passing runs", [site_path], f"expected={expected_fastest}, actual={s.get('fastest')}", "major")
        cost_agents = [a for a in s["agents"] if a.get("cost") is not None]
        expected_cheapest = min(cost_agents, key=lambda a: a["cost"])["id"] if cost_agents else None
        add(checks, f"{sid}.cheapest", s.get("cheapest") == expected_cheapest, f"{sid} cheapest claim matches minimum known normalized cost", [site_path], f"expected={expected_cheapest}, actual={s.get('cheapest')}", "major")
        expected_best = max((a for a in s["agents"] if a.get("process") is not None), key=lambda a: a["process"])["id"]
        add(checks, f"{sid}.best_execution", s.get("processBest") == expected_best, f"{sid} best execution claim matches max execution score", [site_path], f"expected={expected_best}, actual={s.get('processBest')}", "major")

        for a in s.get("agents", []):
            aid = a["id"]
            agent_dir = raw_run / "agents" / aid
            result_path = agent_dir / "result.json"
            verify_path = agent_dir / "verify.log"
            agent_log_path = agent_dir / "agent.log"
            diff_path = agent_dir / "diff.patch"
            add(checks, f"{sid}.{aid}.agent_dir", agent_dir.exists(), f"{sid}/{aid} raw agent directory exists", [agent_dir], "", "blocker")
            for label, p in [("result.json", result_path), ("verify.log", verify_path), ("agent.log", agent_log_path), ("diff.patch", diff_path)]:
                if label == "result.json" and not p.exists() and sid in {"BB-001", "BB-003"}:
                    warn(checks, f"{sid}.{aid}.{label}.exists", f"{sid}/{aid} legacy run lacks result.json; verdict is supported by metrics/results/verify.log instead", [p, verify_path], "legacy early-scenario artifact gap", "major")
                else:
                    add(checks, f"{sid}.{aid}.{label}.exists", p.exists(), f"{sid}/{aid} {label} exists", [p], "", "major")
            if result_path.exists():
                r = load_json(result_path)
                mismatches = []
                for k in ["agentExit", "verifyExit", "verdict", "wall"]:
                    if not eq(a.get(k), r.get(k), k):
                        mismatches.append(f"{k}: site={a.get(k)!r} result={r.get(k)!r}")
                add(checks, f"{sid}.{aid}.result_json_matches_site", not mismatches, f"{sid}/{aid} result.json supports UI verdict/exits/wall", [result_path, site_path], "; ".join(mismatches), "major")
                verdict_ok = (r.get("verdict") == "PASS" and r.get("verifyExit") == 0) or (r.get("verdict") == "FAIL" and r.get("verifyExit") != 0)
                add(checks, f"{sid}.{aid}.verdict_vs_verify_exit", verdict_ok, f"{sid}/{aid} verdict is consistent with verifier exit code", [result_path, verify_path], f"verdict={r.get('verdict')} verifyExit={r.get('verifyExit')}", "blocker")
            if a.get("tokens") is None or a.get("cost") is None:
                ok = a.get("telemetry_strategy") in (None, "unavailable") and aid == "agy"
                add(checks, f"{sid}.{aid}.telemetry_na", ok, f"{sid}/{aid} missing telemetry is explicitly unavailable and scoped to agy", [site_path], f"strategy={a.get('telemetry_strategy')} tokens={a.get('tokens')} cost={a.get('cost')}", "major")
            else:
                tb = a.get("token_breakdown") or {}
                token_total_candidates = [
                    sum(int(tb.get(k) or 0) for k in ["input", "cache_read", "cache_creation", "output"]),
                    sum(int(tb.get(k) or 0) for k in ["input", "cache_read", "cache_creation", "output", "reasoning"]),
                ]
                token_ok = int(a["tokens"]) in token_total_candidates or any(abs(int(a["tokens"]) - t) <= 2 for t in token_total_candidates)
                source_ok = bool(a.get("telemetry_strategy")) and a.get("telemetry_strategy") != "unavailable" and bool(a.get("telemetry_source"))
                if source_ok and token_ok:
                    add(checks, f"{sid}.{aid}.telemetry_provenance", True, f"{sid}/{aid} token/cost telemetry has provenance and plausible token breakdown", [site_path, docs_metrics_path], f"strategy={a.get('telemetry_strategy')} source={a.get('telemetry_source')} token_total_candidates={token_total_candidates} tokens={a.get('tokens')}", "major")
                elif source_ok and not token_ok:
                    warn(checks, f"{sid}.{aid}.telemetry_breakdown_total", f"{sid}/{aid} telemetry has exact provenance but token breakdown does not sum exactly to total", [site_path, docs_metrics_path], f"strategy={a.get('telemetry_strategy')} source={a.get('telemetry_source')} token_total_candidates={token_total_candidates} tokens={a.get('tokens')}", "minor")
                elif not source_ok and sid in {"BB-001", "BB-003"}:
                    warn(checks, f"{sid}.{aid}.telemetry_provenance", f"{sid}/{aid} legacy token/cost values lack per-row telemetry provenance", [site_path, docs_metrics_path], f"strategy={a.get('telemetry_strategy')} source={a.get('telemetry_source')} tokens={a.get('tokens')} cost={a.get('cost')}", "major")
                else:
                    add(checks, f"{sid}.{aid}.telemetry_provenance", False, f"{sid}/{aid} token/cost telemetry has provenance and plausible token breakdown", [site_path, docs_metrics_path], f"strategy={a.get('telemetry_strategy')} source={a.get('telemetry_source')} token_total_candidates={token_total_candidates} tokens={a.get('tokens')}", "major")
            comps = a.get("processComponents") or {}
            if comps:
                comp_sum = round(sum(float(v or 0) for v in comps.values()))
                add(checks, f"{sid}.{aid}.execution_components", comp_sum == a.get("process"), f"{sid}/{aid} execution score equals rounded component sum", [site_path], f"component_sum={comp_sum} process={a.get('process')}", "major")

        if public:
            out = Path("/tmp") / f"cab_public_{s['slug']}.html"
            code, err = run_chrome(f"{base_url.rstrip('/')}/scenarios/{s['slug']}.html", out)
            dom = out.read_text(encoding="utf-8") if out.exists() else ""
            public_ok = code == 0 and "Scenario rail" in dom and "Best execution" in dom and "Execution quality" in dom and 'id="artifactViewer" aria-live="polite" hidden=""' in dom
            add(checks, f"{sid}.public_render", public_ok, f"{sid} public scenario page renders current UI without exposing artifact viewer by default", [out, f"{base_url.rstrip('/')}/scenarios/{s['slug']}.html"], err.strip()[:1000], "blocker")

    referenced_run_ids = {s["runId"] for s in scenarios}
    for root, label in [(RUNS, "runs"), (DOCS / "runs", "docs.runs")]:
        if root.exists():
            orphan_dirs = sorted(p.name for p in root.iterdir() if p.is_dir() and p.name not in referenced_run_ids)
            add(checks, f"{label}.no_orphan_run_dirs", not orphan_dirs, f"{label} has no unreferenced public/conflicting run directories", [root], ", ".join(orphan_dirs), "major")

    latest = data.get("latestScenario") or {}
    expected_latest = scenarios[-1]["id"] if scenarios else None
    add(checks, "site.latestScenario", latest.get("id") == expected_latest, "latestScenario points at the newest scenario in the corpus", [site_path], f"latest={latest.get('id')} expected={expected_latest}", "minor")

    agents_html = (DOCS / "agents.html").read_text(encoding="utf-8") if (DOCS / "agents.html").exists() else ""
    bad_agent_copy = "Pass rate is tied" in agents_html or "100% pass rate conceals" in agents_html
    add(checks, "agents_page.pass_rate_copy", not bad_agent_copy, "Agents page copy does not imply all agents have 100% pass rate", [DOCS / "agents.html"], "", "major")

    status_counts = {k: sum(1 for c in checks if c.status == k) for k in ["PASS", "WARN", "FAIL"]}
    severity_counts = {k: sum(1 for c in checks if c.status != "PASS" and c.severity == k) for k in ["blocker", "major", "minor", "info"]}
    return {
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "repo": "forcewake/coding-agent-battles",
        "commit": subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True, capture_output=True).stdout.strip(),
        "commit_note": "This is the source revision observed when the audit files were generated. A commit that contains regenerated audit files necessarily has a different SHA; compare non-audit files for data changes.",
        "public_base_url": base_url,
        "status_counts": status_counts,
        "severity_counts": severity_counts,
        "overall_status": "FAIL" if status_counts["FAIL"] else "PASS_WITH_WARNINGS" if status_counts["WARN"] else "PASS",
        "checks": [asdict(c) for c in checks],
    }


def write_markdown(ledger: dict[str, Any]) -> str:
    lines = [
        "# Coding Agent Battles — claim ledger audit",
        "",
        f"- Generated: `{ledger['generated_at_utc']}`",
        f"- Commit observed during generation: `{ledger['commit']}`",
        f"- Commit note: {ledger['commit_note']}",
        f"- Overall: **{ledger['overall_status']}**",
        f"- Counts: `{ledger['status_counts']}`",
        f"- Non-pass severities: `{ledger['severity_counts']}`",
        "",
        "## Failed / warning checks",
        "",
    ]
    issues = [c for c in ledger["checks"] if c["status"] != "PASS"]
    if not issues:
        lines.append("No failed or warning checks.")
    else:
        lines.append("| Status | Severity | ID | Claim | Evidence | Details |")
        lines.append("|---|---|---|---|---|---|")
        for c in issues:
            evidence = "<br>".join(f"`{e}`" for e in c["evidence"][:4])
            details = (c.get("details") or "").replace("|", "\\|")[:500]
            lines.append(f"| {c['status']} | {c['severity']} | `{c['id']}` | {c['claim']} | {evidence} | {details} |")
    lines += [
        "",
        "## Audit scope",
        "",
        "This deterministic pass checks committed/public dashboard claims against committed run artifacts:",
        "",
        "- `docs/site-data.json`",
        "- `docs/runs/**/{metrics.json,metrics.md,results.md}`",
        "- `runs/**/{metrics.json,results.md,agents/*/result.json,agents/*/verify.log}`",
        "- optional public rendered scenario pages when `--public` is used",
        "",
        "The ledger intentionally does not infer correctness from private provider databases or uncommitted logs; those are only referenced through already-published telemetry provenance fields.",
    ]
    return "\n".join(lines) + "\n"


def write_prompt(ledger: dict[str, Any]) -> str:
    return f"""# LLM adversarial review prompt — Coding Agent Battles

You are an adversarial benchmark auditor. Do not praise. Find unsupported claims, unfair comparisons, hidden methodology issues, UI wording that overclaims, and any mismatch between dashboard claims and committed evidence.

## Inputs to inspect

- Repository: `forcewake/coding-agent-battles`
- Commit observed during generation: `{ledger['commit']}`
- Commit note: {ledger['commit_note']}
- Public site: `https://forcewake.github.io/coding-agent-battles/`
- Deterministic audit ledger: `docs/audit/claim-ledger.json`
- Telemetry provenance manifest: `docs/audit/telemetry-provenance.json` and `docs/audit/telemetry-provenance.md`
- Human summary: `docs/audit/claim-ledger.md`
- Source data: `docs/site-data.json`
- Public run artifacts: `docs/runs/**/metrics.json`, `docs/runs/**/metrics.md`, `docs/runs/**/results.md`
- Raw committed run artifacts: `runs/**/metrics.json`, `runs/**/results.md`, `runs/**/agents/*/result.json`, `runs/**/agents/*/verify.log`

## Review tasks

1. Check every dashboard-level claim:
   - 12 scenarios / 72 runs / 70 pass / 2 fail
   - fastest / cheapest / best execution per scenario
   - token/cost coverage and `agy` telemetry gaps
2. Check scenario-level claims against committed evidence.
3. Check whether PASS/FAIL is fairly represented.
4. Check whether `Execution quality 0–100 composite` is transparent and not misleading.
5. Check whether normalized public cost is clearly separated from vendor/native cost.
6. Check whether the UI/narrative implies a stronger conclusion than the evidence supports.
7. Check whether any raw/private/provider-specific evidence is referenced in a way that cannot be validated from committed files.

## Output format

Return only JSON:

```json
{{
  "verdict": "APPROVE|APPROVE_WITH_NOTES|REQUEST_CHANGES|REJECT",
  "summary": {{
    "blockers": 0,
    "major": 0,
    "minor": 0
  }},
  "issues": [
    {{
      "severity": "blocker|major|minor",
      "claim": "exact claim being challenged",
      "location": "file/path or public route",
      "expected_evidence": "what would prove it",
      "actual_evidence": "what is present/missing",
      "recommendation": "specific fix"
    }}
  ],
  "methodology_notes": [
    "short note"
  ]
}}
```

Rules:
- Do not invent missing files.
- If evidence is committed and consistent, say no issue.
- Treat deterministic ledger failures as high-priority, but also look for issues it missed.
- Do not evaluate visual taste unless it creates a benchmark-misinterpretation risk.
"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--public", action="store_true", help="also render public GitHub Pages scenario routes with headless Chrome")
    ap.add_argument("--base-url", default="https://forcewake.github.io/coding-agent-battles")
    args = ap.parse_args()
    AUDIT_DIR.mkdir(parents=True, exist_ok=True)
    ledger = audit(public=args.public, base_url=args.base_url)
    (AUDIT_DIR / "claim-ledger.json").write_text(json.dumps(ledger, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    (AUDIT_DIR / "claim-ledger.md").write_text(write_markdown(ledger), encoding="utf-8")
    (AUDIT_DIR / "llm-review-prompt.md").write_text(write_prompt(ledger), encoding="utf-8")
    print(json.dumps({k: ledger[k] for k in ["overall_status", "status_counts", "severity_counts", "commit"]}, indent=2))
    return 1 if ledger["overall_status"] == "FAIL" else 0

if __name__ == "__main__":
    raise SystemExit(main())

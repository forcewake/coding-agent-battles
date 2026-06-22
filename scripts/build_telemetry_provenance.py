#!/usr/bin/env python3
from __future__ import annotations

import json
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DOCS = ROOT / "docs"
AUDIT = DOCS / "audit"


def evidence_level(agent: dict[str, Any], sid: str) -> str:
    strategy = agent.get("telemetry_strategy")
    source = agent.get("telemetry_source") or ""
    if agent.get("tokens") is None or agent.get("cost") is None:
        return "unavailable"
    if sid in {"BB-001", "BB-003"} and not strategy:
        return "legacy_published_metric_without_row_level_provenance"
    if "agent-output.json" in source:
        return "committed_raw_agent_json"
    if "agents/codex-cli/agent.log" in source:
        return "committed_session_id_plus_local_ccusage_extract"
    if "exact projectPath" in source:
        return "local_ccusage_project_path_extract_not_raw_committed"
    if "opencode.log" in source:
        return "local_opencode_log_plus_ccusage_extract_not_raw_committed"
    if "mimocode.db" in source or "MiMoCode SQLite" in source:
        return "local_mimocode_sqlite_extract_not_raw_committed"
    return "sanitized_extracted_metric"


def main() -> None:
    AUDIT.mkdir(parents=True, exist_ok=True)
    data = json.loads((DOCS / "site-data.json").read_text())
    records = []
    for s in data["scenarios"]:
        for a in s["agents"]:
            tb = a.get("token_breakdown") or {}
            records.append({
                "scenario": s["id"],
                "runId": s["runId"],
                "agent": a["id"],
                "verdict": a.get("verdict"),
                "tokens": a.get("tokens"),
                "normalizedPublicCostUsd": a.get("cost"),
                "vendorCostUsd": a.get("vendorCost"),
                "telemetry_strategy": a.get("telemetry_strategy"),
                "telemetry_source": a.get("telemetry_source"),
                "telemetry_session": a.get("telemetry_session"),
                "token_breakdown": tb or None,
                "evidence_level": evidence_level(a, s["id"]),
                "public_audit_note": (
                    "Raw provider store/log is not committed; this row is a sanitized extraction with exact local run/session attribution."
                    if evidence_level(a, s["id"]) in {
                        "committed_session_id_plus_local_ccusage_extract",
                        "local_ccusage_project_path_extract_not_raw_committed",
                        "local_opencode_log_plus_ccusage_extract_not_raw_committed",
                        "local_mimocode_sqlite_extract_not_raw_committed",
                    } else ""
                ),
            })
    counts = Counter(r["evidence_level"] for r in records)
    manifest = {
        "scope": "Public telemetry provenance manifest for Coding Agent Battles",
        "source_commit": data.get("commit") or None,
        "records": records,
        "counts_by_evidence_level": dict(counts),
        "important_limitations": [
            "Some token/cost rows are exact local attributions from ccusage or provider stores whose raw databases/logs are intentionally not committed because they can contain private paths/session data.",
            "Rows marked *_not_raw_committed are auditable as sanitized extracted metrics plus run/session attribution, not as raw-provider replay artifacts.",
            "BB-001 and BB-003 are legacy early runs with published token/cost values but without row-level telemetry provenance fields.",
            "agy/Antigravity token and cost telemetry remains unavailable where no reliable export exists.",
        ],
    }
    (AUDIT / "telemetry-provenance.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n")

    lines = [
        "# Telemetry provenance manifest",
        "",
        "This file exists because token/cost evidence must not be implied to be fully raw-replayable from public files when the source was a local provider store or `ccusage` database.",
        "",
        "## Counts by evidence level",
        "",
        "| Evidence level | Rows |",
        "|---|---:|",
    ]
    for k, v in sorted(counts.items()):
        lines.append(f"| `{k}` | {v} |")
    lines += [
        "",
        "## Limitations",
        "",
    ]
    for item in manifest["important_limitations"]:
        lines.append(f"- {item}")
    lines += [
        "",
        "## Machine-readable manifest",
        "",
        "See `docs/audit/telemetry-provenance.json`.",
    ]
    (AUDIT / "telemetry-provenance.md").write_text("\n".join(lines) + "\n")
    print(json.dumps({"records": len(records), "counts": dict(counts)}, indent=2))


if __name__ == "__main__":
    main()

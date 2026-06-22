#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
DOCS_AUDIT = ROOT / "docs" / "audit"
EXPORT_ROOT = DOCS_AUDIT / "sanitized-telemetry"


def sanitize_source(source: str) -> str:
    source = source or ""
    source = re.sub(r"/home/[^\s,;]+", "[LOCAL_PATH_REDACTED]", source)
    source = re.sub(r"~/(?:[^\s,;]+)", "[HOME_PATH_REDACTED]", source)
    return source


def record_for(scenario: dict[str, Any], agent: dict[str, Any]) -> dict[str, Any]:
    return {
        "schema": "cab.sanitized_telemetry.v1",
        "runId": scenario["runId"],
        "scenarioId": scenario["id"],
        "scenarioName": scenario["name"],
        "agentId": agent["id"],
        "agentLabel": agent.get("label"),
        "model": agent.get("model"),
        "verdict": agent.get("verdict"),
        "wall": agent.get("wall"),
        "tokens": agent.get("tokens"),
        "cost": agent.get("cost"),
        "vendorCost": agent.get("vendorCost"),
        "token_breakdown": agent.get("token_breakdown"),
        "telemetry_strategy": agent.get("telemetry_strategy"),
        "telemetry_source_sanitized": sanitize_source(agent.get("telemetry_source") or ""),
        "telemetry_note": agent.get("telemetry_note"),
        "limitations": [
            "This is a sanitized extracted telemetry record, not a raw provider database/log dump.",
            "Local paths and private provider-store identifiers are redacted or generalized.",
            "Use alongside committed agent evidence for verdict/wall/diff verification.",
        ],
    }


def main() -> int:
    data = json.loads((ROOT / "docs" / "site-data.json").read_text())
    if EXPORT_ROOT.exists():
        shutil.rmtree(EXPORT_ROOT)
    EXPORT_ROOT.mkdir(parents=True, exist_ok=True)
    all_records = []
    for scenario in data.get("scenarios", []):
        run_dir = EXPORT_ROOT / scenario["runId"]
        run_dir.mkdir(parents=True, exist_ok=True)
        for agent in scenario.get("agents", []):
            rec = record_for(scenario, agent)
            all_records.append(rec)
            (run_dir / f"{agent['id']}.json").write_text(json.dumps(rec, indent=2, ensure_ascii=False) + "\n")
    index = {
        "schema": "cab.sanitized_telemetry_index.v1",
        "records": len(all_records),
        "runs": len(data.get("scenarios", [])),
        "description": "Sanitized row-level token/cost telemetry exports for public audit. These intentionally omit raw provider DBs/logs and private local paths.",
        "records_file": "all-records.json",
    }
    (EXPORT_ROOT / "index.json").write_text(json.dumps(index, indent=2, ensure_ascii=False) + "\n")
    (EXPORT_ROOT / "all-records.json").write_text(json.dumps(all_records, indent=2, ensure_ascii=False) + "\n")
    md = [
        "# Sanitized telemetry exports",
        "",
        "This directory contains row-level token/cost telemetry records extracted for public audit.",
        "",
        "These files are **not** raw provider databases or private local logs. They are sanitized exports with local paths redacted, intended to make the published numbers inspectable without leaking private provider stores.",
        "",
        f"- Records: {len(all_records)}",
        f"- Scenario runs: {len(data.get('scenarios', []))}",
        "",
        "See `all-records.json` and per-run `<runId>/<agent>.json` files.",
    ]
    (EXPORT_ROOT / "README.md").write_text("\n".join(md) + "\n")
    print(json.dumps(index, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

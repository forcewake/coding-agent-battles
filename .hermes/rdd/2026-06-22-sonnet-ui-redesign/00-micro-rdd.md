# Micro-RDD — Sonnet/agy UI redesign

Topology: linear (external agy implementation lane)

## User request
The current GitHub Pages UI feels overloaded, inconvenient, and ugly. Run `agy` with Sonnet in maximum/thinking mode and make a cooler UI.

## Scope
- Redesign the static GitHub Pages dashboard in `docs/`.
- Preserve existing committed data contract in `docs/site-data.json` unless a minimal additive field is needed.
- Keep links to raw evidence and methodology.
- Reduce cognitive load: clearer hierarchy, fewer cramped tables above the fold, stronger visual storytelling, premium boardroom/product-console feel.

## Non-goals
- Do not rerun benchmark agents.
- Do not invent new benchmark results.
- Do not add external build dependencies unless justified.

## Verification gates
- `python -m json.tool docs/site-data.json`
- HTML parser smoke for `docs/index.html`
- local HTTP smoke
- browser console check
- visual QA screenshot inspection
- secret scan
- git diff inspection

## Implementation evidence
- First `agy` attempt used the wrong flag shape and ran with default Gemini; no project files were changed. This was rejected.
- Verified correct model syntax with:
  `agy --prompt="Report only current model label." --model="Claude Sonnet 4.6 (Thinking)"` → output `Claude Sonnet 4.6 (Thinking)`.
- Real implementation lane used:
  `agy --prompt="$PROMPT" --model="Claude Sonnet 4.6 (Thinking)" --dangerously-skip-permissions --print-timeout 15m`.
- `/tmp/agy-sonnet-ui-redesign-2.log` contains `model="Claude Sonnet 4.6 (Thinking)"` and repeated selected-model override entries.
- Agent changed `docs/index.html`, `docs/styles.css`, `docs/app.js`; Hermes added small follow-up fix for duplicated mobile nav and badge legend.

## Verification completed
- JSON parse: `docs/site-data.json`.
- HTML parser: `docs/index.html`.
- JS syntax: `node --check docs/app.js`.
- Local HTTP smoke on `http://127.0.0.1:8091/`.
- Browser console: zero errors.
- Visual QA: duplicate nav gone; no blocker-level issues.
- Secret scan: no hits in `docs/` or this RDD artifact.

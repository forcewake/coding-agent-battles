# Brainstorm: Aggregate dashboard + second case

## Orchestration Note
Degraded-controller mode due delegate model routing failure before phase execution.

## Approach 1: Minimal add-on
Run BB-003 and add a small second table below the existing BB-001 page.

Pros: fastest. Cons: does not prove the eventual home aggregate experience.

## Approach 2: Dual-mode single page — Recommended
Turn the existing Pages landing into a corpus home first, then keep run-detail sections below using the latest/selected run. Generate `site-data.json` with both aggregate and latest-run views.

Pros: no build-chain added; preserves current design; immediately demonstrates multi-scenario matrix. Cons: more JS/CSS refactor.

## Approach 3: Multiple pages
Create `/runs/bb-001.html`, `/runs/bb-003.html`, and a new `/index.html` home.

Pros: clean IA. Cons: more files/routes and more time; raw GitHub Pages static routing friction.

## Decision Matrix
| Approach | Speed | Realistic future shape | Risk | Pick |
|---|---:|---:|---:|---|
| Minimal add-on | high | low | low | no |
| Dual-mode single page | medium | high | medium | yes |
| Multiple pages | low | high | medium/high | later |

## Recommended Direction
Use Approach 2: run BB-003 on all six agents, generate aggregate data from BB-001 + BB-003 metrics, and redesign the top of `docs/index.html` as a corpus home while retaining scenario detail/evidence below.

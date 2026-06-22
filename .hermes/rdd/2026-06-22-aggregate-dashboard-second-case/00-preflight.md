# RDD Preflight — Aggregate dashboard + second benchmark case

Topology: swarm

## Scope gate
Implementation work: add an aggregate GitHub Pages dashboard and run/publish one additional benchmark scenario to make corpus-level views real.

## Mode gate
Swarm selected because the work has three separable slices: benchmark scenario/run, aggregate data/model, and visual dashboard.

## Dirty-state gate
Preflight showed clean working tree on `main...origin/main` at commit `3f1f772`.

## Commit gate
User asked to add/run/publish and prior repo workflow uses commits/pushes for evidence; commits are in scope.

## Verification gate
Expected checks: scenario baseline red, per-agent verification, metrics JSON validation, static site validation, local/public Pages HTTP checks, browser console, visual QA.

# Micro-RDD — Remove homepage Evidence section

Topology: micro

## Scope
Remove the homepage section labelled `Evidence` with title `Trace every claim back to committed files`.

## Evidence gathered
- `search_files` found the exact requested copy only in `docs/index.html` lines 166–167.
- Other `Evidence` matches are metrics-table columns, run result headings, logs, or methodology text and are out of scope.

## Decision
Remove the whole homepage artifact-grid section so the requested label/title and its rendered cards disappear together.

## Files changed
- `docs/index.html`

## Verification plan
- Search confirms the removed phrase no longer exists.
- Browser-render homepage and confirm `artifactGrid`/Evidence section is absent and no JS console errors occur.
- Static syntax checks for app/data/html remain green.

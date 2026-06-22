# Candidate Battle Tasks

Status legend: `candidate`, `selected`, `running`, `done`, `rejected`.

| ID | Level | Name | Core skill tested | Repo shape | Verification |
|---|---:|---|---|---|---|
| BB-001 | 0 | Broken CLI argument | Small bugfix, test loop | Tiny Python/Node CLI | Unit tests + CLI smoke |
| BB-002 | 0 | CSV edge-case parser | Edge cases, fixtures | Small library | Provided hidden-ish fixtures + snapshot |
| BB-003 | 1 | Add JSON export to existing CLI | Feature addition without breaking UX | Existing CLI app | Unit tests + golden output |
| BB-004 | 1 | Markdown table normalizer | Text processing, idempotence | Small package | Property tests + examples |
| BB-005 | 2 | FastAPI auth middleware bug | Multi-file backend debugging | API service | pytest + local HTTP smoke |
| BB-006 | 2 | React filter/search UI | Browser-visible frontend feature | Vite/React app | Playwright + screenshot diff |
| BB-007 | 2 | SQLite migration with rollback | Data migration safety | Backend + DB | Migration tests + before/after DB checks |
| BB-008 | 3 | Monorepo dependency upgrade | Tooling, CI, cross-package failures | JS/Python monorepo | Full test/lint/typecheck matrix |
| BB-009 | 3 | Observability instrumentation | Enterprise feature, non-functional requirements | Web API | Tests + logs/traces shape smoke |
| BB-010 | 3 | PDF/DOCX extraction quality fix | Real-world document handling | Existing OSS repo | Corpus fixtures + output scoring |
| BB-011 | 4 | Long-horizon greenfield mini-product | Planning + implementation + browser proof | New full-stack app | E2E flow + artifact quality rubric |
| BB-012 | 4 | Unknown repo leverage task | Find/use OSS repo to solve user-facing task | External repo integration | Repro script + output validator |

## First recommended battle pack

1. **BB-001** — calibration: verifies command discipline and basic test loop.
2. **BB-005** — realistic backend bug, enough context to punish shallow edits.
3. **BB-006** — browser/screenshot evidence exposes agents that only satisfy tests.
4. **BB-008** — dependency/tooling pain; good for CLI autonomy comparison.
5. **BB-011** — long-horizon vertical slice; best for qualitative UX/architecture differences.

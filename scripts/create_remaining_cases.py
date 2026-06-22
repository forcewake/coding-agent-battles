#!/usr/bin/env python3
from __future__ import annotations

import json
import os
import shutil
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS = ROOT / "tasks"

def w(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")

def pyproject(path: Path, name: str, package: str, deps: list[str] | None = None) -> None:
    deps = deps or []
    w(path / "pyproject.toml", f'''
    [project]
    name = "{name}"
    version = "0.1.0"
    requires-python = ">=3.11"
    dependencies = {json.dumps(deps)}

    [tool.setuptools.packages.find]
    include = ["{package}*"]
    ''')
    w(path / ".gitignore", "__pycache__/\n.pytest_cache/\n.venv/\n*.egg-info/\nnode_modules/\ndist/\n")

def verify_py(path: Path, extra: str = "") -> None:
    w(path / "verify.py", f'''
    #!/usr/bin/env python3
    from __future__ import annotations
    import json, os, subprocess, sys, venv
    from pathlib import Path
    ROOT = Path(__file__).resolve().parent
    VENV = ROOT / ".venv"
    if not VENV.exists():
        venv.EnvBuilder(with_pip=True).create(VENV)
    py = VENV / "bin" / "python"
    def run(cmd, **kw):
        print("[run]", " ".join(map(str, cmd)), flush=True)
        return subprocess.run(cmd, cwd=ROOT, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, **kw)
    r = run([str(py), "-m", "pip", "install", "-q", "-e", ".", "pytest"])
    print(r.stdout, end="")
    if r.returncode: sys.exit(r.returncode)
    r = run([str(py), "-m", "pytest", "-q"])
    print(r.stdout, end="")
    if r.returncode: sys.exit(r.returncode)
    {extra}
    print("[verify_exit_code] 0")
    ''')

# BB-002 CSV edge-case parser
base = TASKS / "BB-002-csv-edge-case-parser"
shutil.rmtree(base, ignore_errors=True)
fix = base / "fixture"
pyproject(fix, "bb002-csvedge", "bb002_csvedge")
w(base / "task.md", '''
# BB-002 — CSV edge-case parser

Fix the CSV summary library. The current parser uses naive `str.split(',')`, so quoted commas, escaped quotes, and blank rows are mishandled.

## Requirements
- Use proper CSV parsing semantics.
- Preserve the public API: `summarize_people_csv(text: str) -> dict`.
- Ignore fully blank rows.
- Count valid rows and group by city.
- Keep deterministic sorted city keys.
- `python verify.py` must pass.
''')
w(fix / "bb002_csvedge/__init__.py", "from .parser import summarize_people_csv\n__all__ = ['summarize_people_csv']\n")
w(fix / "bb002_csvedge/parser.py", '''
    def summarize_people_csv(text: str) -> dict:
        lines = [line for line in text.splitlines() if line.strip()]
        header = lines[0].split(",")
        rows = [dict(zip(header, line.split(","))) for line in lines[1:]]
        by_city = {}
        for row in rows:
            city = row.get("city", "").strip()
            by_city[city] = by_city.get(city, 0) + 1
        return {"rows": len(rows), "by_city": dict(sorted(by_city.items()))}
''')
w(fix / "tests/test_parser.py", '''
    from bb002_csvedge import summarize_people_csv

    def test_quoted_commas_and_escaped_quotes():
        data = 'name,city,note\n"Doe, Jane",Amsterdam,"likes ""quoted"" text"\nJohn,Rotterdam,plain\n\nAlice,Amsterdam,"x,y"\n'
        assert summarize_people_csv(data) == {"rows": 3, "by_city": {"Amsterdam": 2, "Rotterdam": 1}}
''')
verify_py(fix)

# BB-004 Markdown table normalizer
base = TASKS / "BB-004-markdown-table-normalizer"
shutil.rmtree(base, ignore_errors=True)
fix = base / "fixture"
pyproject(fix, "bb004-mdtable", "bb004_mdtable")
w(base / "task.md", '''
# BB-004 — Markdown table normalizer

Implement a deterministic Markdown table normalizer.

## Requirements
- Normalize pipe tables into padded columns.
- Preserve non-table text.
- Output must be idempotent: `normalize(normalize(x)) == normalize(x)`.
- Separator row must be normalized to `---` per column.
- `python verify.py` must pass.
''')
w(fix / "bb004_mdtable/__init__.py", "from .normalizer import normalize_markdown_tables\n__all__ = ['normalize_markdown_tables']\n")
w(fix / "bb004_mdtable/normalizer.py", '''
    def normalize_markdown_tables(markdown: str) -> str:
        return markdown
''')
w(fix / "tests/test_normalizer.py", '''
    from bb004_mdtable import normalize_markdown_tables

    INPUT = "Intro\n\n| name|score |\n|---|---|\n|Pi| 96|\n|OpenCode|88 |\n\nOutro\n"
    EXPECTED = "Intro\n\n| name     | score |\n| ---      | ---   |\n| Pi       | 96    |\n| OpenCode | 88    |\n\nOutro\n"

    def test_normalizes_table_and_preserves_text():
        assert normalize_markdown_tables(INPUT) == EXPECTED

    def test_idempotent():
        once = normalize_markdown_tables(INPUT)
        assert normalize_markdown_tables(once) == once
''')
verify_py(fix)

# BB-005 FastAPI auth middleware bug
base = TASKS / "BB-005-fastapi-auth-middleware-bug"
shutil.rmtree(base, ignore_errors=True)
fix = base / "fixture"
pyproject(fix, "bb005-authapi", "bb005_authapi", ["fastapi", "httpx"])
w(base / "task.md", '''
# BB-005 — FastAPI auth middleware bug

Fix the auth dependency so `/admin` requires `Authorization: Bearer secret-token` while `/healthz` stays public.

## Requirements
- No token => `/admin` returns 401.
- Wrong token => `/admin` returns 403.
- Correct token => 200 with `{"status":"ok","scope":"admin"}`.
- `/healthz` remains 200 without auth.
- `python verify.py` must pass.
''')
w(fix / "bb005_authapi/__init__.py", "")
w(fix / "bb005_authapi/app.py", '''
    from fastapi import Depends, FastAPI, Header, HTTPException

    app = FastAPI()

    def require_admin(authorization: str | None = Header(default=None)):
        # BUG: accidentally accepts every request.
        return True

    @app.get("/healthz")
    def healthz():
        return {"status": "healthy"}

    @app.get("/admin")
    def admin(_: bool = Depends(require_admin)):
        return {"status": "ok", "scope": "admin"}
''')
w(fix / "tests/test_auth.py", '''
    from fastapi.testclient import TestClient
    from bb005_authapi.app import app

    client = TestClient(app)

    def test_healthz_public():
        assert client.get('/healthz').status_code == 200

    def test_admin_requires_token():
        assert client.get('/admin').status_code == 401
        assert client.get('/admin', headers={'Authorization': 'Bearer wrong'}).status_code == 403
        r = client.get('/admin', headers={'Authorization': 'Bearer secret-token'})
        assert r.status_code == 200
        assert r.json() == {'status': 'ok', 'scope': 'admin'}
''')
verify_py(fix, '''
    r = run([str(py), "-c", "from fastapi.testclient import TestClient; from bb005_authapi.app import app; c=TestClient(app); print(c.get('/healthz').json())"])
    print(r.stdout, end="")
    if r.returncode: sys.exit(r.returncode)
''')

# BB-006 React-ish filter/search UI (dependency-free static JS)
base = TASKS / "BB-006-react-filter-search-ui"
shutil.rmtree(base, ignore_errors=True)
fix = base / "fixture"
w(base / "task.md", '''
# BB-006 — React filter/search UI

Fix the browser-visible search/filter state model. The UI is represented by a small dependency-free module to keep the benchmark reproducible.

## Requirements
- `filterItems(items, query, tag)` must be case-insensitive.
- Query searches title and description.
- Tag `all` disables tag filtering.
- Result order is stable by original input order.
- Empty result state text must be `No matching agents`.
- `python verify.py` must pass.
''')
w(fix / "package.json", '{"type":"module","scripts":{"test":"node --test tests/filter.test.mjs"}}\n')
w(fix / "src/filter.mjs", '''
    export function filterItems(items, query = '', tag = 'all') {
      // BUG: title-only, case-sensitive, ignores tag.
      return items.filter(item => item.title.includes(query));
    }
    export function emptyStateText() { return 'Nothing here'; }
''')
w(fix / "tests/filter.test.mjs", '''
    import assert from 'node:assert/strict';
    import test from 'node:test';
    import { filterItems, emptyStateText } from '../src/filter.mjs';

    const items = [
      { title: 'OpenCode', description: 'fast GLM coding lane', tags: ['fast', 'cheap'] },
      { title: 'Codex', description: 'robust reasoning', tags: ['robust'] },
      { title: 'Pi', description: 'cost-process champion', tags: ['cheap'] },
    ];

    test('query searches title and description case-insensitively', () => {
      assert.deepEqual(filterItems(items, 'GLM', 'all').map(x => x.title), ['OpenCode']);
      assert.deepEqual(filterItems(items, 'reason', 'all').map(x => x.title), ['Codex']);
    });

    test('tag filter combines with query and keeps order', () => {
      assert.deepEqual(filterItems(items, '', 'cheap').map(x => x.title), ['OpenCode', 'Pi']);
      assert.deepEqual(filterItems(items, 'code', 'cheap').map(x => x.title), ['OpenCode']);
    });

    test('empty state copy is product quality', () => {
      assert.equal(emptyStateText(), 'No matching agents');
    });
''')
w(fix / "verify.py", '''
    #!/usr/bin/env python3
    import subprocess, sys
    r = subprocess.run(['node', '--test', 'tests/filter.test.mjs'], text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(r.stdout, end='')
    if r.returncode: sys.exit(r.returncode)
    print('[verify_exit_code] 0')
''')
w(fix / ".gitignore", "node_modules/\n")

# BB-007 SQLite migration rollback
base = TASKS / "BB-007-sqlite-migration-rollback"
shutil.rmtree(base, ignore_errors=True)
fix = base / "fixture"
pyproject(fix, "bb007-migrate", "bb007_migrate")
w(base / "task.md", '''
# BB-007 — SQLite migration with rollback

Fix migration rollback safety.

## Requirements
- `upgrade(conn)` adds nullable `email` column to `users` and preserves rows.
- `downgrade(conn)` removes the `email` column and preserves `id/name` rows.
- Running upgrade twice must not duplicate/fail.
- `python verify.py` must pass.
''')
w(fix / "bb007_migrate/__init__.py", "from .migration import upgrade, downgrade\n__all__ = ['upgrade','downgrade']\n")
w(fix / "bb007_migrate/migration.py", '''
    def upgrade(conn):
        conn.execute('ALTER TABLE users ADD COLUMN email TEXT')
        conn.commit()

    def downgrade(conn):
        # BUG: destructive rollback loses data.
        conn.execute('DROP TABLE users')
        conn.commit()
''')
w(fix / "tests/test_migration.py", '''
    import sqlite3
    from bb007_migrate import upgrade, downgrade

    def cols(conn):
        return [r[1] for r in conn.execute('PRAGMA table_info(users)')]

    def seed():
        conn = sqlite3.connect(':memory:')
        conn.execute('CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT NOT NULL)')
        conn.executemany('INSERT INTO users (id, name) VALUES (?, ?)', [(1, 'Ada'), (2, 'Linus')])
        conn.commit()
        return conn

    def test_upgrade_idempotent_and_preserves_rows():
        conn = seed()
        upgrade(conn); upgrade(conn)
        assert cols(conn) == ['id', 'name', 'email']
        assert conn.execute('SELECT id, name FROM users ORDER BY id').fetchall() == [(1, 'Ada'), (2, 'Linus')]

    def test_downgrade_removes_email_preserves_rows():
        conn = seed(); upgrade(conn)
        conn.execute("UPDATE users SET email='ada@example.test' WHERE id=1")
        downgrade(conn)
        assert cols(conn) == ['id', 'name']
        assert conn.execute('SELECT id, name FROM users ORDER BY id').fetchall() == [(1, 'Ada'), (2, 'Linus')]
''')
verify_py(fix)

# BB-008 monorepo dependency upgrade
base = TASKS / "BB-008-monorepo-dependency-upgrade"
shutil.rmtree(base, ignore_errors=True)
fix = base / "fixture"
w(base / "task.md", '''
# BB-008 — Monorepo dependency upgrade

A shared utility changed its API from `slugify(text)` to `makeSlug(text, options)`. Fix the app package without breaking compatibility tests.

## Requirements
- Update app code to use the new shared API.
- Preserve stable slugs: lowercase, trim, collapse non-alphanumerics to single dash.
- Do not reintroduce the old `slugify` export.
- `python verify.py` must pass.
''')
w(fix / "package.json", '{"type":"module","scripts":{"test":"node --test packages/*/test/*.test.mjs"}}\n')
w(fix / "packages/shared/index.mjs", '''
    export function makeSlug(text, options = {}) {
      const lower = options.lower !== false;
      const source = lower ? text.toLowerCase() : text;
      return source.trim().replace(/[^a-z0-9]+/gi, '-').replace(/^-|-$/g, '');
    }
''')
w(fix / "packages/app/index.mjs", '''
    import { slugify } from '../shared/index.mjs';
    export function scenarioPath(name) {
      return `/scenarios/${slugify(name)}.html`;
    }
''')
w(fix / "packages/app/test/app.test.mjs", '''
    import assert from 'node:assert/strict';
    import test from 'node:test';
    import { scenarioPath } from '../index.mjs';
    import * as shared from '../../shared/index.mjs';

    test('scenario path uses upgraded shared slug API', () => {
      assert.equal(scenarioPath(' BB 008: Dependency Upgrade! '), '/scenarios/bb-008-dependency-upgrade.html');
    });
    test('old slugify API is not reintroduced', () => {
      assert.equal('slugify' in shared, false);
    });
''')
w(fix / "verify.py", '''
    #!/usr/bin/env python3
    import subprocess, sys
    r = subprocess.run(['node', '--test', 'packages/*/test/*.test.mjs'], shell=True, text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    print(r.stdout, end='')
    if r.returncode: sys.exit(r.returncode)
    print('[verify_exit_code] 0')
''')
w(fix / ".gitignore", "node_modules/\n")

# BB-009 observability instrumentation
base = TASKS / "BB-009-observability-instrumentation"
shutil.rmtree(base, ignore_errors=True)
fix = base / "fixture"
pyproject(fix, "bb009-observe", "bb009_observe", ["fastapi", "httpx"])
w(base / "task.md", '''
# BB-009 — Observability instrumentation

Add request logging middleware with safe structured logs.

## Requirements
- Every request appends one JSON line to `app.state.events`.
- Event fields: `method`, `path`, `status_code`, `duration_ms`, `correlation_id`.
- Use incoming `x-correlation-id` when present; otherwise generate a non-empty id.
- Do not log authorization headers or request bodies.
- `python verify.py` must pass.
''')
w(fix / "bb009_observe/__init__.py", "")
w(fix / "bb009_observe/app.py", '''
    from fastapi import FastAPI
    app = FastAPI()
    app.state.events = []

    @app.get('/items/{item_id}')
    def get_item(item_id: str):
        return {'item_id': item_id}
''')
w(fix / "tests/test_observe.py", '''
    from fastapi.testclient import TestClient
    from bb009_observe.app import app

    def test_structured_request_event_without_secrets():
        app.state.events.clear()
        c = TestClient(app)
        r = c.get('/items/42', headers={'x-correlation-id': 'corr-123', 'authorization': 'Bearer SECRET'})
        assert r.status_code == 200
        assert len(app.state.events) == 1
        event = app.state.events[0]
        assert event['method'] == 'GET'
        assert event['path'] == '/items/42'
        assert event['status_code'] == 200
        assert event['correlation_id'] == 'corr-123'
        assert isinstance(event['duration_ms'], (int, float)) and event['duration_ms'] >= 0
        assert 'authorization' not in event and 'SECRET' not in repr(event)

    def test_generates_correlation_id():
        app.state.events.clear()
        c = TestClient(app)
        c.get('/items/99')
        assert app.state.events[0]['correlation_id']
''')
verify_py(fix)

# BB-010 DOCX extraction quality fix (OOXML zip, no external deps)
base = TASKS / "BB-010-docx-extraction-quality-fix"
shutil.rmtree(base, ignore_errors=True)
fix = base / "fixture"
pyproject(fix, "bb010-docx", "bb010_docx")
w(base / "task.md", '''
# BB-010 — DOCX extraction quality fix

Fix OOXML/DOCX text extraction quality.

## Requirements
- Extract paragraphs and table cell text from `word/document.xml` inside a `.docx` zip.
- Preserve paragraph/table reading order.
- Decode XML entities.
- Join extracted text lines with `\n`.
- `python verify.py` must pass.
''')
w(fix / "bb010_docx/__init__.py", "from .extract import extract_docx_text\n__all__ = ['extract_docx_text']\n")
w(fix / "bb010_docx/extract.py", '''
    from pathlib import Path
    from zipfile import ZipFile
    import re

    def extract_docx_text(path: str | Path) -> str:
        with ZipFile(path) as zf:
            xml = zf.read('word/document.xml').decode('utf-8')
        # BUG: only paragraph text, misses tables and entities.
        parts = re.findall(r'<w:p>.*?<w:t[^>]*>(.*?)</w:t>.*?</w:p>', xml, flags=re.S)
        return '\n'.join(parts)
''')
w(fix / "tests/test_extract.py", '''
    from pathlib import Path
    from zipfile import ZipFile
    from bb010_docx import extract_docx_text

    def make_docx(path: Path):
        xml = ''' + repr('''<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>Intro &amp; overview</w:t></w:r></w:p><w:tbl><w:tr><w:tc><w:p><w:r><w:t>Cell A</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>Cell B</w:t></w:r></w:p></w:tc></w:tr></w:tbl><w:p><w:r><w:t>Done</w:t></w:r></w:p></w:body></w:document>''') + '''
        with ZipFile(path, 'w') as zf:
            zf.writestr('word/document.xml', xml)

    def test_extracts_paragraphs_and_table_cells(tmp_path):
        p = tmp_path / 'sample.docx'
        make_docx(p)
        assert extract_docx_text(p) == 'Intro & overview\nCell A\nCell B\nDone'
''')
verify_py(fix)

# BB-011 greenfield mini-product
base = TASKS / "BB-011-greenfield-mini-product"
shutil.rmtree(base, ignore_errors=True)
fix = base / "fixture"
pyproject(fix, "bb011-miniproduct", "bb011_miniproduct", ["fastapi", "httpx"])
w(base / "task.md", '''
# BB-011 — Long-horizon greenfield mini-product

Build a tiny benchmark registry API from tests/spec.

## Requirements
- Provide `create_app()` in `bb011_miniproduct.app` returning a FastAPI app.
- `POST /scenarios` accepts `{id,name,level}` and stores it in memory.
- Duplicate id returns 409.
- `GET /scenarios` returns scenarios sorted by level then id.
- `GET /healthz` returns `{"status":"ok"}`.
- `python verify.py` must pass.
''')
w(fix / "bb011_miniproduct/__init__.py", "")
w(fix / "bb011_miniproduct/app.py", '''
    # Intentionally incomplete greenfield product.
    def create_app():
        raise NotImplementedError('build the API')
''')
w(fix / "tests/test_app.py", '''
    from fastapi.testclient import TestClient
    from bb011_miniproduct.app import create_app

    def test_scenario_registry_flow():
        client = TestClient(create_app())
        assert client.get('/healthz').json() == {'status': 'ok'}
        assert client.post('/scenarios', json={'id':'BB-011','name':'Mini product','level':4}).status_code == 201
        assert client.post('/scenarios', json={'id':'BB-002','name':'CSV','level':0}).status_code == 201
        assert client.post('/scenarios', json={'id':'BB-011','name':'Dup','level':4}).status_code == 409
        assert client.get('/scenarios').json() == [
          {'id':'BB-002','name':'CSV','level':0},
          {'id':'BB-011','name':'Mini product','level':4},
        ]
''')
verify_py(fix)

# BB-012 unknown repo leverage task
base = TASKS / "BB-012-unknown-repo-leverage-task"
shutil.rmtree(base, ignore_errors=True)
fix = base / "fixture"
pyproject(fix, "bb012-leverage", "bb012_leverage")
w(base / "task.md", '''
# BB-012 — Unknown repo leverage task

Use the provided `vendor/textkit` helper instead of reimplementing tokenization incorrectly.

## Requirements
- `summarize(text)` returns top words with counts, sorted by count desc then word asc.
- Use `vendor.textkit.words` so punctuation/case handling matches the vendor helper.
- Ignore stopwords from `vendor.textkit.STOPWORDS`.
- Return at most 3 entries as list of `{word,count}` dicts.
- `python verify.py` must pass.
''')
w(fix / "vendor/textkit.py", '''
    import re
    STOPWORDS = {'the', 'and', 'of', 'to', 'a'}
    def words(text: str) -> list[str]:
        return re.findall(r"[a-z0-9]+", text.lower())
''')
w(fix / "vendor/__init__.py", "")
w(fix / "bb012_leverage/__init__.py", "from .summary import summarize\n__all__ = ['summarize']\n")
w(fix / "bb012_leverage/summary.py", '''
    def summarize(text: str):
        # BUG: whitespace split keeps punctuation/case and stopwords.
        counts = {}
        for token in text.split():
            counts[token] = counts.get(token, 0) + 1
        return [{'word': w, 'count': c} for w, c in counts.items()][:3]
''')
w(fix / "tests/test_summary.py", '''
    from bb012_leverage import summarize

    def test_uses_vendor_tokenization_and_stopwords():
        text = 'The agent, agent; AGENT! cost-of-change and process process to verify.'
        assert summarize(text) == [
            {'word': 'agent', 'count': 3},
            {'word': 'process', 'count': 2},
            {'word': 'change', 'count': 1},
        ]
''')
verify_py(fix)

print('created remaining case fixtures')

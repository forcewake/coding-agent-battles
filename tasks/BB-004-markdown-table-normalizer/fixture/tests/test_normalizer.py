from bb004_mdtable import normalize_markdown_tables


INPUT = """Intro

| name|score |
|---|---|
|Pi| 96|
|OpenCode|88 |

Outro
"""
EXPECTED = """Intro

| name     | score |
| ---      | ---   |
| Pi       | 96    |
| OpenCode | 88    |

Outro
"""


def test_normalizes_table_and_preserves_text():
    assert normalize_markdown_tables(INPUT) == EXPECTED


def test_idempotent():
    once = normalize_markdown_tables(INPUT)
    assert normalize_markdown_tables(once) == once

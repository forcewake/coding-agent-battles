"""Deterministic Markdown pipe-table normalizer."""

from __future__ import annotations

import re

# A separator cell looks like `---`, `:--`, `--:`, or `:--:`.
_SEP_CELL = re.compile(r"^:?-+:?$")


def _split_row(line: str) -> list[str]:
    """Split a pipe-table row into stripped cell contents.

    Handles rows both with and without leading/trailing pipes.
    """
    stripped = line.strip()
    parts = stripped.split("|")
    # Drop the empty strings produced by a leading/trailing pipe.
    if parts and parts[0].strip() == "":
        parts = parts[1:]
    if parts and parts[-1].strip() == "":
        parts = parts[:-1]
    return [p.strip() for p in parts]


def _is_pipe_row(line: str) -> bool:
    return "|" in line and line.strip() != ""


def _is_separator(line: str) -> bool:
    if "|" not in line:
        return False
    cells = _split_row(line)
    if not cells:
        return False
    return all(_SEP_CELL.match(c) for c in cells)


def _normalize_table(table_lines: list[str]) -> list[str]:
    rows = [_split_row(line) for line in table_lines]
    ncols = max(len(r) for r in rows)
    # Pad any short rows so all rows share the column count.
    rows = [r + [""] * (ncols - len(r)) for r in rows]

    # Column widths come from every row except the separator (row index 1).
    widths = [0] * ncols
    for idx, row in enumerate(rows):
        if idx == 1:
            continue
        for c in range(ncols):
            widths[c] = max(widths[c], len(row[c]))

    rendered = []
    for idx, row in enumerate(rows):
        if idx == 1:
            cells = ["---".ljust(widths[c]) for c in range(ncols)]
        else:
            cells = [row[c].ljust(widths[c]) for c in range(ncols)]
        rendered.append("| " + " | ".join(cells) + " |")
    return rendered


def normalize_markdown_tables(markdown: str) -> str:
    """Normalize pipe tables into padded columns.

    Non-table text is preserved verbatim. The result is idempotent.
    """
    lines = markdown.split("\n")
    output: list[str] = []
    i = 0
    n = len(lines)
    while i < n:
        line = lines[i]
        # A table begins with a header row followed immediately by a
        # separator row, then continues with consecutive pipe rows.
        if _is_pipe_row(line) and i + 1 < n and _is_separator(lines[i + 1]):
            table_lines = [line, lines[i + 1]]
            j = i + 2
            while j < n and _is_pipe_row(lines[j]) and not _is_separator(lines[j]):
                table_lines.append(lines[j])
                j += 1
            output.extend(_normalize_table(table_lines))
            i = j
        else:
            output.append(line)
            i += 1
    return "\n".join(output)

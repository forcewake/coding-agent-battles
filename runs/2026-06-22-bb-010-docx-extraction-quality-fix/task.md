# BB-010 — DOCX extraction quality fix

Fix OOXML/DOCX text extraction quality.

## Requirements
- Extract paragraphs and table cell text from `word/document.xml` inside a `.docx` zip.
- Preserve paragraph/table reading order.
- Decode XML entities.
- Join extracted text lines with `
`.
- `python verify.py` must pass.

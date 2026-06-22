from pathlib import Path
from zipfile import ZipFile
import re


def extract_docx_text(path: str | Path) -> str:
    with ZipFile(path) as zf:
        xml = zf.read('word/document.xml').decode('utf-8')
    # BUG: only paragraph text, misses tables and entities.
    parts = re.findall(r'<w:p>.*?<w:t[^>]*>(.*?)</w:t>.*?</w:p>', xml, flags=re.S)
    return '\n'.join(parts)

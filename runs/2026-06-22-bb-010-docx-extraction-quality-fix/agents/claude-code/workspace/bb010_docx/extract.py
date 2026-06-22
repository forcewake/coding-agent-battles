from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET

# ponytail: ElementTree walks <w:p> in document order (cells hold <w:p>, so
# tables come out in reading order) and decodes entities for free — replaces the
# fragile regex.
W = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'


def extract_docx_text(path: str | Path) -> str:
    with ZipFile(path) as zf:
        root = ET.fromstring(zf.read('word/document.xml'))
    lines = [
        ''.join(t.text or '' for t in p.iter(f'{W}t'))
        for p in root.iter(f'{W}p')
    ]
    return '\n'.join(lines)

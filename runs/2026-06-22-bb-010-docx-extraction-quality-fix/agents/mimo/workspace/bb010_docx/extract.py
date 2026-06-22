from pathlib import Path
from zipfile import ZipFile
from xml.etree import ElementTree as ET

_W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def extract_docx_text(path: str | Path) -> str:
    with ZipFile(path) as zf:
        xml = zf.read('word/document.xml').decode('utf-8')
    root = ET.fromstring(xml)
    lines = []
    for p in root.iter(f'{{{_W}}}p'):
        text = ''.join((t.text or '') for t in p.iter(f'{{{_W}}}t'))
        lines.append(text)
    return '\n'.join(lines)

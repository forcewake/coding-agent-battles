from pathlib import Path
from zipfile import ZipFile
import xml.etree.ElementTree as ET

W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
_P = f'{{{W_NS}}}p'
_T = f'{{{W_NS}}}t'


def extract_docx_text(path: str | Path) -> str:
    with ZipFile(path) as zf:
        xml = zf.read('word/document.xml').decode('utf-8')
    root = ET.fromstring(xml)
    lines = []
    # iter() yields descendants in document order, including paragraphs
    # nested inside table cells, so reading order is preserved.
    for p in root.iter(_P):
        texts = [t.text or '' for t in p.iter(_T)]
        lines.append(''.join(texts))
    return '\n'.join(lines)

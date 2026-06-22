from pathlib import Path
from xml.etree import ElementTree
from zipfile import ZipFile


def extract_docx_text(path: str | Path) -> str:
    with ZipFile(path) as zf:
        xml = zf.read('word/document.xml')

    root = ElementTree.fromstring(xml)
    ns = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'
    parts = [
        ''.join(t.text or '' for t in paragraph.iter(f'{ns}t'))
        for paragraph in root.iter(f'{ns}p')
    ]
    return '\n'.join(parts)

from pathlib import Path
from zipfile import ZipFile

from bb010_docx import extract_docx_text


def make_docx(path: Path):
    xml = '<w:document xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main"><w:body><w:p><w:r><w:t>Intro &amp; overview</w:t></w:r></w:p><w:tbl><w:tr><w:tc><w:p><w:r><w:t>Cell A</w:t></w:r></w:p></w:tc><w:tc><w:p><w:r><w:t>Cell B</w:t></w:r></w:p></w:tc></w:tr></w:tbl><w:p><w:r><w:t>Done</w:t></w:r></w:p></w:body></w:document>'
    with ZipFile(path, 'w') as zf:
        zf.writestr('word/document.xml', xml)


def test_extracts_paragraphs_and_table_cells(tmp_path):
    p = tmp_path / 'sample.docx'
    make_docx(p)
    assert extract_docx_text(p) == 'Intro & overview\nCell A\nCell B\nDone'

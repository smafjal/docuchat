from docuchat.data_loader import chunk_documents, load_pdfs
from pathlib import Path

def test_load_and_chunk():
    folder = Path("tests/sample_pdfs")
    docs = load_pdfs(folder)
    chunks = chunk_documents(docs)
    assert len(docs) > 0
    assert len(chunks) > 0
    assert isinstance(chunks[0].page_content, str)
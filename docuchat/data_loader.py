from pathlib import Path
from typing import List
from langchain.schema import Document
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from .config import CHUNK_SIZE, CHUNK_OVERLAP

class PDFProcessor:
    def __init__(self, pdf_dir: Path):
        self.pdf_dir = pdf_dir
        self.documents: List[Document] = []
        self.chunks: List[Document] = []

    def load_pdfs(self) -> List[Document]:
        self.documents = []
        for pdf_path in self.pdf_dir.glob("*.pdf"):
            loader = PyPDFLoader(str(pdf_path))
            self.documents.extend(loader.load())
        return self.documents

    def chunk_documents(self, chunk_size=CHUNK_SIZE, chunk_overlap=CHUNK_OVERLAP) -> List[Document]:
        splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
        self.chunks = splitter.split_documents(self.documents)
        return self.chunks

    def process(self) -> List[Document]:
        self.load_pdfs()
        return self.chunk_documents()

from pathlib import Path
import typer
from .vector import VectorStoreManager
from .config import API_NAME
from .data_loader import PDFProcessor
from .agent import RetrieverAgent

app = typer.Typer()

@app.command()
def ingest(pdfdir: str = "data/pdfs"):
    folder_path = Path(pdfdir)
    if not folder_path.exists():
        raise FileNotFoundError(f"{pdfdir} not found")

    print("\U0001F4C4 Loading PDFs...")
    pdf_processor = PDFProcessor(folder_path)
    pdf_processor.process()
    print(f"\U0001F4D6 Loaded and chunked into {len(pdf_processor.chunks)} parts")

    print("\U0001F9E0 Embedding...")
    VectorStoreManager(API_NAME).create_vector_store(pdf_processor.chunks)
    print("✅ Vector store created.")

@app.command()
def chat():
    app_agent = RetrieverAgent(api_name=API_NAME)
    print("\n🤖 Docuchat ready! Type your questions (exit to quit)")
    while True:
        question = input("You: ").strip()
        if not question:
            continue

        if question.lower() in {"exit", "quit"}:
            break

        result = app_agent.invoke(question)
        print("\n=== ANSWER ===")
        print(result['messages'][-1].content)

if __name__ == "__main__":
    app()

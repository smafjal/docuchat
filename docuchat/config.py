from pathlib import Path

PDF_DIR = Path("./data/pdfs")
VECTOR_STORE_DIR = Path("./data/vector_store")

CHUNK_SIZE = 500
CHUNK_OVERLAP = 100


# API_NAME = "openai"
# LLM_MODEL_NAME = "gpt-4o-mini"
# EMBED_MODEL_NAME = "text-embedding-3-small"

API_NAME = "groq"
LLM_MODEL_NAME = "llama3-8b-8192"
EMBED_MODEL_NAME = "BAAI/bge-large-en-v1.5"
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from docuchat import config
from langchain_huggingface import HuggingFaceEmbeddings

class VectorStoreManager:
    def __init__(self, api_name: str = "openai"):
        if api_name == "openai":
            self.embedding_fn = OpenAIEmbeddings(model=config.EMBED_MODEL_NAME)
        elif api_name == "groq":
            self.embedding_fn = HuggingFaceEmbeddings(model_name=config.EMBED_MODEL_NAME)
        else:
            raise ValueError(f"Invalid API name: {api_name}")

    def create_vector_store(self, chunks: list[Document]) -> None:
        Chroma.from_documents(chunks, embedding=self.embedding_fn, persist_directory=str(config.VECTOR_STORE_DIR))

    def get_retriever(self):
        return Chroma(persist_directory=str(config.VECTOR_STORE_DIR), embedding_function=self.embedding_fn).as_retriever(search_kwargs={"k": 3})


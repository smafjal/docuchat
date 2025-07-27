from langchain_chroma import Chroma
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain_openai import OpenAIEmbeddings
from langchain.schema import Document
from docuchat import config
from langchain_huggingface import HuggingFaceEmbeddings
from .prompt import RETRIEVER_QUERY_PROMPT

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

    def get_retriever(self, k: int = 3):
        return Chroma(persist_directory=str(config.VECTOR_STORE_DIR), embedding_function=self.embedding_fn).as_retriever(search_kwargs={"k": k})

    def get_multi_query_retriever(self, llm):
        retriever = Chroma(persist_directory=str(config.VECTOR_STORE_DIR), embedding_function=self.embedding_fn).as_retriever()
        return MultiQueryRetriever.from_llm(
            retriever=retriever, 
            llm=llm,
            prompt=RETRIEVER_QUERY_PROMPT,
        )
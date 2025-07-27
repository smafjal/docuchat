from dotenv import load_dotenv
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_openai import ChatOpenAI
from langchain_groq import ChatGroq
from .config import LLM_MODEL_NAME

load_dotenv()

def get_llm(api_name: str = "openai"):
    common_args = {
        "temperature": 0,
        "streaming": True,
    }
    if api_name == "openai":
        return ChatOpenAI(**common_args, callbacks=[StreamingStdOutCallbackHandler()])
    elif api_name == "groq":
        return ChatGroq(**common_args, model=LLM_MODEL_NAME)
    else:
        raise ValueError(f"Unsupported LLM provider: {api_name}")

from typing import Annotated, Sequence, TypedDict
import warnings
from langgraph.graph import StateGraph, END
from langgraph.graph.message import add_messages
from langchain.schema import BaseMessage
from langchain_core.messages import SystemMessage, ToolMessage, HumanMessage
from langchain_core.tools import Tool
from .config import API_NAME
from .prompt import SYSTEM_PROMPT_1, SYSTEM_PROMPT_2
from .vector import VectorStoreManager
from .llm import get_llm

warnings.filterwarnings("ignore")

class AgentState(TypedDict):
    messages: Annotated[Sequence[BaseMessage], add_messages]


class RetrieverAgent:
    """
    Manages LangGraph flow for agent with retrieval capability.
    """

    def __init__(self, api_name: str = API_NAME):
        self.retriever = VectorStoreManager(api_name).get_retriever()
        self.tools = self.build_tools()
        self.tools_dict = {tool.name: tool for tool in self.tools}
        self.llm = get_llm(api_name).bind_tools(self.tools)
        self.graph = self.build_graph()
        self.system_prompt = SYSTEM_PROMPT_1

    def invoke(self, questions: str) -> AgentState:
        messages = [HumanMessage(content=questions)]
        return self.graph.invoke({"messages": messages})

    def build_tools(self):
        return [
            Tool.from_function(
                name="retriever_tool",
                description="Retrieves relevant information from a collection of PDF documents using vector-based semantic search.",
                func=self.retriever_tool,
            )
        ]

    def build_graph(self):
        graph = StateGraph(AgentState)
        graph.add_node("llm", self.invoke_llm)
        graph.add_node("knowledge_retriever", self.knowledge_retriever)

        graph.add_conditional_edges(
            "llm",
            self.should_continue,
            {
                True: "knowledge_retriever",
                False: END,
            },
        )
        graph.add_edge("knowledge_retriever", "llm")
        graph.set_entry_point("llm")

        return graph.compile()

    def should_continue(self, state: AgentState) -> bool:
        """Determine if LLM made tool calls."""
        last_message = state["messages"][-1]
        return hasattr(last_message, "tool_calls") and len(last_message.tool_calls) > 0

    def invoke_llm(self, state: AgentState) -> AgentState:
        """Call LLM with current message state."""
        messages = [SystemMessage(content=self.system_prompt)] + list(state["messages"])
        response = self.llm.invoke(messages)
        return {"messages": [response]}

    def knowledge_retriever(self, state: AgentState) -> AgentState:
        """Invoke tools based on LLM tool calls."""
        results = []
        for tcall in state["messages"][-1].tool_calls:
            tname = tcall["name"]
            if tname not in self.tools_dict:
                result = "Incorrect Tool Name. Please select from available tools."
            else:
                targs = tcall["args"].get("query", "")
                result = self.tools_dict[tname].invoke(targs)

            results.append(
                ToolMessage(tool_call_id=tcall["id"], name=tname, content=str(result))
            )
        return {"messages": results}

    def retriever_tool(self, query: str) -> str:
        """
        Tool: Retrieves relevant information from a collection of PDF documents using vector-based semantic search.
        """
        docs = self.retriever.invoke(query)
        if not docs:
            return "No relevant information found in the documents."

        return "\n\n".join(
            f"Document {i + 1}:\n{doc.page_content}" for i, doc in enumerate(docs)
        )

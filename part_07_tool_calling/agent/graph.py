"""Part 7 — LangGraph graph wiring tool-calling ReAct loop."""

from typing import Annotated
from langchain_core.messages import BaseMessage
from langgraph.graph import StateGraph, START, END
from langgraph.graph.message import add_messages
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.checkpoint.memory import MemorySaver
from typing_extensions import TypedDict

from tools import ALL_TOOLS
from agent.react_agent import build_react_agent, get_system_message


class AgentState(TypedDict):
    messages: Annotated[list[BaseMessage], add_messages]


def build_tool_agent_graph(llm, checkpointer=None):
    """Build and compile the ReAct tool-calling agent graph.

    Graph flow:
        START → llm_node ──(has tool calls)──► tool_node → llm_node
                          └──(no tool calls)──► END
    """
    react_llm = build_react_agent(llm)
    tool_node = ToolNode(tools=ALL_TOOLS)

    def llm_node(state: AgentState) -> AgentState:
        """Call the LLM (with tools bound). Prepend system message on first turn."""
        messages = state["messages"]
        system = get_system_message()
        if not messages or messages[0].type != "system":
            messages = [system] + list(messages)
        response = react_llm.invoke(messages)
        return {"messages": [response]}

    graph = StateGraph(AgentState)
    graph.add_node("llm", llm_node)
    graph.add_node("tools", tool_node)

    graph.add_edge(START, "llm")
    # tools_condition returns "tools" if tool_calls present, otherwise END
    graph.add_conditional_edges("llm", tools_condition)
    graph.add_edge("tools", "llm")

    return graph.compile(checkpointer=checkpointer or MemorySaver())

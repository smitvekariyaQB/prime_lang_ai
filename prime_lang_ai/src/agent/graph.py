"""LangGraph single-node graph template.

Returns a predefined response. Replace logic and configuration as needed.
"""

from __future__ import annotations

from dataclasses import dataclass

from langgraph.graph import StateGraph, START, END
from langgraph.runtime import Runtime
from typing_extensions import TypedDict
from typing import TypedDict, Annotated, Literal
from agent.prompt import general_prompt
from agent.schema import GeneralResponse
from typing import TypedDict, List
from agent.llm import gemini_llm
from agent.tools import handle_attack_query, handle_elon_query
from langgraph.prebuilt import ToolNode, tools_condition
from langchain_core.messages import BaseMessage, HumanMessage, AIMessage
from langgraph.graph.message import add_messages

class Context(TypedDict):
    """Context parameters for the agent.

    Set these when creating assistants OR when invoking the graph.
    See: https://langchain-ai.github.io/langgraph/cloud/how-tos/configuration_cloud/
    """

    my_configurable_param: str


class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]

tools = [handle_attack_query, handle_elon_query]
tool_node = ToolNode(tools)

def call_model(state: AgentState):

    llm_with_tools = gemini_llm.bind_tools(tools)

    result = llm_with_tools.invoke(state["messages"])

    return {"messages": [result]}


graph = StateGraph(AgentState)
graph.add_node("agent", call_model)
graph.add_node("tools", tool_node)

graph.add_edge(START, "agent")
graph.add_conditional_edges("agent", tools_condition)
graph.add_edge("tools", END)


workflow = graph.compile(name="New Graph")
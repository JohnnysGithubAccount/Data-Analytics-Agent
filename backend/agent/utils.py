from dataclasses import dataclass
from typing import Optional, Any, Dict, Annotated, List

import pandas as pd
from langchain.retrievers import MultiQueryRetriever
from langchain_ollama import ChatOllama
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, AIMessage
from langgraph.graph import StateGraph, END
import base64
import os


# === Define the shared graph state ===
class State(TypedDict):
    input_prompt: str
    overview: str
    agent_responses: List[AnyMessage]
    command: str
    next_agent: str
    file_name: str
    called_agents: List[str]


# === Plot the graph ===
def plot_graph(graph, path="graph.png"):
    png_data = graph.get_graph().draw_mermaid_png(max_retries=5, retry_delay=2.0)

    # Save to a file
    with open(path, "wb") as f:
        f.write(png_data)

    print(f"[INFO] Saved graph at {path}")
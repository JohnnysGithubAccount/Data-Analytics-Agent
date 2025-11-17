from dataclasses import dataclass
from typing import Optional, Any, Dict, Annotated, List

from langchain.retrievers import MultiQueryRetriever
from langchain_ollama import ChatOllama
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, AIMessage
from langgraph.graph import StateGraph, END
import base64
import os


class ManagerRouter:
    def __init__(self):
        self.mapping = {
            "planning_agent": "planning",
            "chart_drawing_agent": "drawing",
            "chart_analysis_agent": "chart_analyze",
            "insights_agent": "insights",
            "end": "finish"
        }

    def __call__(self, state):
        print("ROUTER MANAGER")
        """
            NEXT_AGENT: <agent_name>
            CLEAR_PREVIOUS_AGENT_HISTORY: either YES or NO
            COMMAND: <instructions for that agent>
        """

        next_agent = state["next_agent"]
        routing_destination = "try_again"
        try:
            routing_destination = self.mapping[next_agent]
        except KeyError:
            pass
        print(f"[ROUTER] Routing to {routing_destination}")
        return routing_destination


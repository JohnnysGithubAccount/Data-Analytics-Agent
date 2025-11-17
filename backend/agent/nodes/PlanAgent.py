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
from typing import Dict, Any, List

class PlanAgent:
    def __init__(self, llm):
        """
        llm is your external model (ChatOllama, ChatOpenAI, GPT, etc.)
        """
        self.llm = llm

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        print("PLAN AGENT")
        command = state["command"]
        overview = state["overview"]  # dataset summary, columns, sample rows, etc.

        prompt = f"""
            You are a Data Visualization Planner Agent.
            
            Your job:
            - Understand the dataset from the overview.
            - Interpret the user's command.
            - Produce a list of chart tasks needed to satisfy the command.
            - ONLY propose charts that are relevant and possible given the columns.
            - Do not give any other comments other than python list of charts needed to be drawn.
            
            USER COMMAND:
            {command}
            
            DATAFRAME OVERVIEW (this is the overview of the tabular data you need to understand):
            {overview}
            
            Follow strictly to the output format. Do not add anything else but the answer like in the output format.
            OUTPUT FORMAT (STRICT):
            A Python list of chart instruction strings, e.g.:
            
            ["Plot salary distribution", "Bar chart of average age per department"]
        """

        response = self.llm.invoke(prompt)

        # Extract chart plan safely
        try:
            # Find the Python list in the response
            start = response.find("[")
            end = response.rfind("]") + 1
            chart_plan = eval(response[start:end])
            if not isinstance(chart_plan, list):
                chart_plan = [command]
        except:
            chart_plan = [command]

        # state["reasoning"] = response
        # state["chart_plan"] = chart_plan
        state["agent_responses"] = ["Response from planning_agent", response]
        # state["agent_responses"].extend(chart_plan)

        # print(f"[PLAN AGENT RESPONSE]")
        # for line in response.content.splitlines():
        #     print(f"\t[LINE] {line}")
        #
        # print("CHART PLAN")
        # for plan in chart_plan:
        #     print(f"\t{plan}")

        return state

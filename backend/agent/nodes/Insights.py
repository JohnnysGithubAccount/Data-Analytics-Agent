import textwrap
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


import os
import textwrap
from langchain_core.messages import AIMessage

class InsightsAgent:
    def __init__(self, llm, txt_folder: str = "analysis", chunk_size=1200):
        self.llm = llm
        self.txt_folder = txt_folder
        self.chunk_size = chunk_size

    def _chunk_text(self, text):
        return textwrap.wrap(text, self.chunk_size)

    def _extract_insights_from_chunk(self, chunk, running_insights):
        """
        Extract NEW insights from an incoming chunk and merge them with
        the global insight memory WITHOUT summarizing.
        This behaves like a professional senior data analyst.
        """

        prompt = f"""
            You are a world-class Senior Data Analyst.
            
            You are NOT summarizing.
            You are extracting INSIGHTS.
            
            Below is the current GLOBAL INSIGHT MEMORY:
            ---------------------
            {running_insights}
            ---------------------
            
            Below is a NEW ANALYSIS CHUNK from another report:
            ---------------------
            {chunk}
            ---------------------
            
            TASK:
            1. Extract **new patterns, anomalies, correlations, and behaviors** from this chunk.
            2. If the chunk contradicts old insights, update them.
            3. If the chunk adds new insights, merge them.
            4. Keep the global insight memory sharp, structured, and high-signal.
            
            Write the updated INSIGHT MEMORY (not a summary).
            Make it:
            - concise
            - analytical
            - factual
            - data-driven
            - non-repetitive
        """

        result = self.llm.invoke(prompt)
        return result.content if isinstance(result, AIMessage) else result

    def _process_file(self, path, running_insights):
        with open(path, "r", encoding="utf-8") as f:
            full_text = f.read().strip()

        chunks = self._chunk_text(full_text)
        for chunk in chunks:
            running_insights = self._extract_insights_from_chunk(chunk, running_insights)

        return running_insights

    def __call__(self, state):
        print("INSIGHTS AGENT")

        running_insights = "No insights yet."

        for file in os.listdir(self.txt_folder):
            if file.endswith(".txt"):
                path = os.path.join(self.txt_folder, file)
                running_insights = self._process_file(path, running_insights)

        # ---- Final professional insight report ----
        final_prompt = f"""
            You now have the FULL GLOBAL INSIGHT MEMORY from all reports:
            
            {running_insights}
            
            Produce a final **Professional Insights Report** including:
            
            - Key trends & behavioral patterns  
            - Strong correlations  
            - Anomalies and red flags  
            - Hypotheses and causal reasoning  
            - Predictions  
            - Strategic & actionable recommendations  
            
            Tone: data scientist + business strategist.
            Style: concise, high-impact, expert.
        """

        final_output = self.llm.invoke(final_prompt)

        os.makedirs("insights", exist_ok=True)
        insights_file = os.path.join("insights", "insights.txt")
        insights_text = final_output.content if isinstance(final_output, AIMessage) else final_output
        with open(insights_file, "w", encoding="utf-8") as f:
            f.write(insights_text)

        # print(f"[INSIGHTS AGENT RESPONSE]")
        # for line in final_output.content.splitlines():
        #     print(f"\t[LINE] {line}")

        return {
            "agent_responses": [
                "This is the insights from the data. Task is finished by the insights_agent, so end the process now with END.",
                final_output.content
            ],
            "df": None
        }

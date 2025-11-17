import json
import sys
import os

import numpy as np
import pandas as pd
from langchain.retrievers import MultiQueryRetriever
from langchain_community.vectorstores import Chroma
from langchain_core.messages import ToolMessage
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder, PromptTemplate
from langchain_core.runnables import RunnablePassthrough, RunnableLambda

from langchain_ollama import ChatOllama, OllamaEmbeddings
from langchain_neo4j import Neo4jVector
from langgraph.constants import END
from langgraph.graph import StateGraph, START
from langgraph.checkpoint.memory import InMemorySaver
from langchain.schema import SystemMessage, HumanMessage, AIMessage

from backend.agent.tool import tools_list


# === Manager (Supervisor) ===
class Manager:
    def __init__(self, llm):
        self.llm = llm

    def __call__(self, state):
        print("MANAGER AGENT")
        system_prompt = f"""
            You are the Supervisor Agent. You in charge of control worker agents for doing step by step process of analyzing user's tabular data.
            You will receive a summarization of the tabular data. Based on that to decide tasks
            
            The worker agents are the follows:
            - planning_agent: This agent will look at the overview and give out the plan what charts should be drawn to best analyze the table. It give give you a python list of what needed to be done. If you see that, and it seems fine, just go ahead a move on the next model.
            - chart_drawing_agent: This agent will draw charts with the dataframe and what you asked it to draw.
            - chart_analysis_agent: This agent is powered by a VLM, and it will give some professional analysis from those charts.
            - insights_agent: This agent will summarize and infer the core and deep insights from the analysis of the chart_analysis_agent.
            - END: this is when everything is done. No further action is needed to be done.
            
            And the process should go from planning, drawing charts, analyze those charts, and then giving professional insights.
            If a member agent has done its job very well and moved on to another member, do not called it again.
            You have to move forward, if you see called agents, you shouldn't called them back unless it's the last agent you work with (which means you are still working with it) and you need it to continue do something with its task.
            Decide the next agent and provide instructions. You must answer in this exact format.
            You are not allowed to goes backward in the pipeline. Which means (planning_agent can't be called after the drawing_chart_agent has already been called).
            It has to go from planning_agent to chart_drawing_agent to chart_analysis_agent to insights_agent to END. You are not allowed to go backward on this sequence.
            
            If you have done with one one agent already and moving on to the next agent, you have to answer 'YES' for CLEAR_PREVIOUS_AGENT_HISTORY. If you still have something to do what that agent, give 'NO'.
            If everything is done, put END in <agent_name> place. 
            You have to stick strictly to this response format.
            WHY_NEXT_AGENT: why you choose to move on to the next agent? Or what is wrong with the past model response that make you want to ask it to redo its work?
            
            Format:
            WHY_NEXT_AGENT: <why_next_agent>
            NEXT_AGENT: <agent_name>
            CLEAR_PREVIOUS_AGENT_HISTORY: either YES or NO
            COMMAND: <instructions for that agent>
        """

        prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder(variable_name="overview"),
                MessagesPlaceholder(variable_name="agent_responses"),
                MessagesPlaceholder(variable_name="called_agents"),
                ("human", "{description_prompt}")
            ]
        )
        chain = prompt | self.llm

        user_description_prompt = state["input_prompt"]
        overview = state["overview"]
        agent_responses = state.get("agent_responses", [])
        called_agent = state.get("called_agents", ["This is a list of called agents"])

        # print("Invoking")
        input_dict = {
            "description_prompt": user_description_prompt,
            "overview": [overview],
            "called_agents": called_agent,
            "agent_responses": agent_responses,
        }
        # print(f"[INFO] Input dictionary")
        # for key, value in input_dict.items():
        #     print(f"\t{key}: {value}")
        manager_command = chain.invoke(input_dict)

        lines = manager_command.content.replace("*", "").split("\n")

        why_next_agent = lines[0].replace("NEXT_AGENT:", "").strip().lower()
        next_agent = lines[1].replace("NEXT_AGENT:", "").strip().lower()
        clear_agent_responses = lines[2].replace("CLEAR_PREVIOUS_AGENT_HISTORY:", "").strip().lower()

        raw_cmd = "\n".join(lines[3:])
        command = raw_cmd.replace("COMMAND:", "", 1).strip()

        if clear_agent_responses == "yes":
            state["agent_responses"] = []

        # print(f"[MANAGER RESPONSE]")
        # for line in manager_command.content.splitlines():
        #     print(f"\t[LINE] {line}")

        if next_agent not in called_agent:
            called_agent.append(next_agent)

        return {
            "command": command,
            "next_agent": next_agent,
            "agent_responses": state.get("agent_responses", []),
            "called_agents": called_agent,
        }


def main():
    pass


if __name__ == "__main__":
    # Test the langgraph node
    main()
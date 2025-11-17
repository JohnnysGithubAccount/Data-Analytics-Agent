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


# === agent ===
class Agent:
    def __init__(self, llm):
        self.llm = llm

        self.system_prompt = """
        You are a professional data analyst. 
        You analyze user tabular data for professional insights.
        """

    def __call__(self, state):
        retriever = state["retriever"]
        input_message = state["input_prompt"]

        template = """Answer the question based ONLY on the following context:
        {context}
        Question: {question}
        """

        prompt = ChatPromptTemplate.from_template(template)

        chain = (
                {"context": retriever, "question": RunnablePassthrough()}
                | prompt
                | self.llm
                | StrOutputParser()
        )
        print("Invoking")
        llm_response = chain.invoke(
            {
                "question": input_message,
                "input": input_message
            }
        )

        return {"messages": state["messages"] + [llm_response]}



# === Tool execution ===
class ToolExecution:
    """A node that runs the tools requested in the last AIMessage."""

    def __init__(self, tools: list) -> None:
        self.tools_by_name = {tool.name: tool for tool in tools}
        # print(self.tools_by_name)

    def __call__(self, inputs: dict):
        if messages := inputs.get("messages", []):
            message = messages[-1]
        else:
            raise ValueError("No message found in input")
        outputs = []

        for tool_call in message.tool_calls:
            if 'function' in str(tool_call['args']):
                tool_call["args"] = tool_call["args"]["parameters"]
            try:
                tool_result = self.tools_by_name[tool_call["name"]].invoke(
                    tool_call["args"]
                )
                tool_result["room"] = tool_call["args"]["room"]
            except Exception as e:
                print(e)

            outputs.append(
                ToolMessage(
                    content=json.dumps(tool_result),
                    name=tool_call["name"],
                    tool_call_id=tool_call["id"],
                )
            )
        new_messages = messages + outputs
        return {"messages": new_messages}


# === Router ===
class Router:
    def __init__(self):
        pass

    def __call__(self, state):
        # Support both list-of-messages and dict-with-messages
        if isinstance(state, list):
            ai_message = state[-1]
        elif messages := state.get("messages", []):
            ai_message = messages[-1]
        else:
            raise ValueError(f"No messages found in input state: {state}")

        if hasattr(ai_message, "tool_calls") and ai_message.tool_calls:
            return "drawing graphs"

        return "finish"
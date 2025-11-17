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


# === Rag ===
class RAG:
    def __init__(self, llm, embedding_model):
        self.llm = llm

        if embedding_model:
            self.embedding_model = embedding_model
        else:
            self.embedding_model = OllamaEmbeddings(
                model="nomic-embed-text",
                show_progress=False
            )

        self.system_prompt = (
            "You are an AI assistant. Answer the user's questions based on the column names: "
            # "Id, order_id, name, sales, refund, and status."
        )

    def __call__(self, state):
        # Build dynamic prompt
        query_prompt = ChatPromptTemplate.from_messages([
            ("system", self.system_prompt),
            ("human", "{input}")
        ])

        QUERY_PROMPT = PromptTemplate(
            input_variables=["question"],
            template="""You are an AI assistant. Answer the user's questions based on the column namesl. Original question: {question}"""
        )

        vector_db_name = state["vector_db_name"]
        print(vector_db_name)
        abs_path = r"D:\UsingSpace\Projects\Artificial Intelligent\Agent\Data Analytics Agent\backend\vector_dbs"
        persist_directory = f"./vector_dbs/{vector_db_name}"
        persist_dir = os.path.join(abs_path, vector_db_name)
        vector_db = Chroma(
            persist_directory=persist_directory,
            embedding_function=self.embedding_model,
            collection_name=vector_db_name
        )

        # Create retriever
        retriever = MultiQueryRetriever.from_llm(
            vector_db.as_retriever(),
            self.llm,
            prompt=QUERY_PROMPT
        )

        if "input_prompt" in state:
            print("[DEBUG] Running retrieval test for:", state["input_prompt"])
            results = retriever.invoke(state["input_prompt"])
            print(f"[DEBUG] Retrieved {len(results)} docs:")
            for i, doc in enumerate(results[:3]):  # Show top 3
                print(f"  [DOC {i}] {doc.page_content[:200]}...\n")

        return {"retriever": retriever}

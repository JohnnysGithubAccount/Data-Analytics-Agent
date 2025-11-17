import asyncio
import os, sys
import time

project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.append(project_root)

import uvicorn
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.responses import StreamingResponse
import shutil, pandas as pd
import json
import numpy as np
import traceback

from langchain_core.runnables import RunnableConfig
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma

from .data_review import get_data_from_file
from .utils import get_list_uploaded_file, init_stored_file, clear_folder
from agent.graph import graph


# embedding_model = OllamaEmbeddings(model="nomic-embed-text", show_progress=False)
text_splitter = RecursiveCharacterTextSplitter(chunk_size=7500, chunk_overlap=100)

# === upload single file ===
def upload_singple_file(file, upload_dir, stored_files):
    file_path = os.path.join(upload_dir, file.filename)

    # Save uploaded file
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Store file info in memory
    stored_files[file.filename] = {
        "path": file_path,
        "prompt": ""
    }

    return {"message": "File uploaded successfully!", "filename": file.filename}


# === upload file and prompt ===
def upload_file_and_prompt(file, prompt, upload_dir, stored_files):
    clear_folder("insights")
    clear_folder("analysis")
    clear_folder("charts")

    file_path = os.path.join(upload_dir, file.filename)

    # Ensure upload directory exists
    os.makedirs(upload_dir, exist_ok=True)

    # Save uploaded file
    with open(file_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    # Load file into a Pandas DataFrame
    df = None
    try:
        if file.filename.lower().endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file.filename.lower().endswith((".xls", ".xlsx")):
            df = pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file type. Only CSV and Excel files are allowed.")
    except Exception as e:
        return {"error": f"Failed to load file: {str(e)}"}

    # Store file info in memory
    stored_files[file.filename] = {
        "path": file_path,
        "prompt": prompt,
    }

    data = df.to_string(index=False)
    # chunks = text_splitter.split_text(data)

    file_base = os.path.splitext(os.path.basename(file_path))[0]
    persist_dir = os.path.join("vector_dbs", file_base)  # e.g., vector_dbs/myfile/
    os.makedirs(persist_dir, exist_ok=True)

    # vector_db = Chroma.from_texts(
    #     texts=chunks,
    #     embedding=embedding_model,
    #     persist_directory=persist_dir,
    #     collection_name=file_base,
    # )

    if file_base not in stored_files:
        print("Skip saving since it has already exist")
        # vector_db.persist()
        print(f"[INFO] Vector DB saved at: {persist_dir}")

        # Save the prompt to a text file in the same folder
        prompt_path = os.path.join(persist_dir, "prompt.txt")
        with open(prompt_path, "w", encoding="utf-8") as f:
            f.write(prompt)


    # Init graph and stuff
    # status = graph_inference(
    #     user_prompt=prompt,
    #     file_name=file.filename
    # )

    return {"message": "File uploaded and processed successfully!", "filename": file.filename}


def graph_inference(user_prompt, file_name):
    """
    FUNCTION INSIDE ENDPOINTS HAVE TO RETURN SOMETHING
    :param user_prompt:
    :param file_name:
    :return:
    """
    config = RunnableConfig(
        run_name="graph_test_run",
        configurable={"thread_id": "test-thread-1"},
        recursion_limit=100
    )
    input_state = {
        "input_prompt": user_prompt,
        "file_name": file_name
    }
    for step in graph.stream(input_state, config):
        for node_name, output in step.items():
            print("=" * 30)

    return {"status": "Finished"}


async def graph_streaming_results(file_name, prompt):
    """
    Stream graph node updates in real-time via SSE.
    frontend: EventSource('http://localhost:8000/graph_stream/<file_name>')
    """
    print("called this")

    async def event_generator():
        # RunnableConfig for graph streaming
        config = RunnableConfig(
            run_name="graph_sse_run",
            configurable={"thread_id": f"sse-{file_name}"},
            recursion_limit=100
        )
        input_state = {
            "input_prompt": prompt,
            "file_name": file_name
        }

        # Stream through the graph
        for step in graph.stream(input_state, config):
            for node_name, output in step.items():
                # Yield SSE formatted message
                print(node_name)
                yield f"data: {json.dumps({'node_name': node_name})}\n\n"
                # optional tiny delay to avoid overloading frontend
                await asyncio.sleep(0.01)

        # Signal end of stream
        yield f"data: {json.dumps({'node_name': 'END'})}\n\n"
        time.sleep(1)
        yield f"data: {json.dumps({'done': True})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")


async def fake_graph_stream(file_name, prompt):
    nodes_sequence = [
        "data_overview",
        "manager_agent",
        "planning_agent",
        "manager_agent",
        "chart_drawing_agent",
        "manager_agent",
        "chart_analysis_agent",
        "manager_agent",
        "insights_agent",
        "manager_agent",
        "END"
    ]

    async def event_generator():
        for node_name in nodes_sequence:
            print(f"Streaming node: {node_name}")
            yield f"data: {json.dumps({'node_name': node_name})}\n\n"
            await asyncio.sleep(1)

        # Final done signal
        yield f"data: {json.dumps({'done': True})}\n\n"

    return StreamingResponse(event_generator(), media_type="text/event-stream")
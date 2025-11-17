import time

import uvicorn
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import StreamingResponse
from fastapi.responses import JSONResponse
import os, shutil, pandas as pd
import json
import numpy as np
import traceback

from utils.insights import insights_results
from utils.analysis import analysis_results
from utils.upload import upload_file_and_prompt, fake_graph_stream, graph_streaming_results
from utils.upload import upload_singple_file
from utils.data_review import get_data_from_file
from utils.utils import get_list_uploaded_file, init_stored_file
from utils.utils import make_json_safe, delete_file
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# Allow frontend requests
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # adjust in production
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)
# app.mount("/charts", StaticFiles(directory="backend"), name="charts")
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CHART_DIR = os.path.join(BASE_DIR, "charts")

# Mount static assets (CHARTS ONLY)
app.mount("/charts", StaticFiles(directory=CHART_DIR), name="charts")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Store uploaded files info
stored_files = init_stored_file(UPLOAD_DIR)

# ==============================================================
# UPLOAD PAGE

# === Upload file only endpoint ===
@app.post("/upload_file")
async def upload_file(file: UploadFile = File(...)):
    return upload_singple_file(file, UPLOAD_DIR, stored_files)


# === Upload endpoint ===
@app.post("/upload")
async def upload_file(file: UploadFile = File(...), prompt: str = Form(...)):
    return upload_file_and_prompt(file, prompt, UPLOAD_DIR, stored_files)


# ==============================================================
# DATA REVIEW PAGE

# === Data review endpoint ===
@app.get("/data-review")
def data_review(filename: str):
    return get_data_from_file(filename, stored_files)


# ==============================================================
# FILE MANAGING PANEL

# === Get list upload files ===
@app.get("/uploaded-files")
def list_uploaded_files():
    return get_list_uploaded_file(UPLOAD_DIR)


# === Delete a specific file by filename ===
@app.delete("/uploaded-files/{filename}")
def delete_uploaded_file(filename: str):
    return delete_file(filename, stored_files)


# ==============================================================
# ANALYSIS PAGE (GRAPHS)
@app.get("/analysis")
async def analysis():
    return analysis_results()


# ==============================================================
# INSIGHTS PAGE (AGENTS COMMENTS)
@app.get("/insights")
async def insights():
    return insights_results()


# ==============================================================
# GRAPH STREAMING
@app.get("/graph_stream")
async def graph_stream(file_name: str, prompt: str = ""):
    # return await fake_graph_stream(file_name, prompt)
    return await graph_streaming_results(file_name, prompt)

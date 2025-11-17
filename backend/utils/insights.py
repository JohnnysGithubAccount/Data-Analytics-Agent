from fastapi import FastAPI
from fastapi.responses import JSONResponse
import os


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSIGHTS_FILE = os.path.join(BASE_DIR, "insights", "insights.txt")

def insights_results():
    if not os.path.exists(INSIGHTS_FILE):
        return JSONResponse(content={"content": ""})

    with open(INSIGHTS_FILE, "r", encoding="utf-8") as f:
        text = f.read()

    return JSONResponse(content={"content": text})

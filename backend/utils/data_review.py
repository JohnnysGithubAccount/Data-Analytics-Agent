import uvicorn
from fastapi import FastAPI, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import os, shutil, pandas as pd
import json
import numpy as np
import traceback
from .utils import make_json_safe


# === get the data from file for review ===
def get_data_from_file(filename, stored_files):
    if filename not in stored_files:
        return JSONResponse(status_code=404, content={"error": "File not found"})

    file_path = stored_files[filename]["path"]
    try:
        if file_path.endswith(".csv"):
            df = pd.read_csv(file_path)
        elif file_path.endswith((".xls", ".xlsx")):
            df = pd.read_excel(file_path)
        else:
            return JSONResponse(status_code=400, content={"error": "Unsupported file type"})

        # Replace infinities and NaNs
        df = df.replace([np.inf, -np.inf], np.nan).where(pd.notnull(df), None)

        # Convert DataFrame → dict
        preview = df.to_dict(orient="records")

        # Make the preview JSON-safe
        preview = make_json_safe(preview)

        return JSONResponse(content={"filename": filename, "preview": preview})

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

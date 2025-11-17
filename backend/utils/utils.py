import json
import shutil

import numpy as np
import pandas as pd
from datetime import datetime, date
from fastapi.responses import JSONResponse
import os


# === Init stored file ===
def init_stored_file(upload_dir):
    stored_files = {}
    for fname in os.listdir(upload_dir):
        fpath = os.path.join(upload_dir, fname)
        if os.path.isfile(fpath):
            stored_files[fname] = {"path": fpath}

    return stored_files


# === Make json safe ===
def make_json_safe(obj):
    """Recursively convert objects to JSON-serializable types."""
    if isinstance(obj, (datetime, date)):
        return obj.isoformat()
    elif isinstance(obj, (np.integer,)):
        return int(obj)
    elif isinstance(obj, (np.floating,)):
        return float(obj)
    elif isinstance(obj, (np.ndarray, list, tuple)):
        return [make_json_safe(x) for x in obj]
    elif isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    elif pd.isna(obj):
        return None
    return obj


# === Delete saved file ===
def delete_file(filename, stored_files):
    if filename not in stored_files:
        print(stored_files)
        return JSONResponse(status_code=404, content={"error": "File not found"})

    file_path = stored_files[filename]["path"]
    folder_name = filename.replace(".csv", "").replace(".xlsx", "")
    vector_db_dir = f"vector_dbs/{folder_name}"

    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print("removing file")

        if vector_db_dir and os.path.exists(vector_db_dir):
            print("removing vector db")
            shutil.rmtree(vector_db_dir)

        # Remove from stored_files dictionary
        del stored_files[filename]
        return {"message": f"File '{filename}' deleted successfully"}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# === Get list uploaded file ===
def get_list_uploaded_file(upload_dir):
    try:
        files = os.listdir(upload_dir)
        # Only show CSV/XLS/XLSX
        files = [f for f in files if f.endswith((".csv", ".xls", ".xlsx"))]
        return {"files": files}
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


# === Clear file in the folder ===
def clear_folder(folder_path: str):
    """
    Deletes all files in the given folder but keeps the folder itself.
    """
    if not os.path.exists(folder_path):
        print(f"Folder does not exist: {folder_path}")
        return

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)  # remove file or link
            elif os.path.isdir(file_path):
                # optional: remove subfolders too
                import shutil
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

    print(f"All files cleared in folder: {folder_path}")
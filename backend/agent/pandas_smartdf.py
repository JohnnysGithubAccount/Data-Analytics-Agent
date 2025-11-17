import os
import logging
import matplotlib
import pandas as pd
import psutil
import subprocess
from pandasai import SmartDataframe
from pandasai.llm.local_llm import LocalLLM
import time

# ---------------------------
# FIX LOGGING ERRORS ON WINDOWS
# ---------------------------
logging.disable(logging.CRITICAL)
matplotlib.use("Agg")

# ---------------------------
# 1. Create fake CSV
# ---------------------------
df_fake = pd.DataFrame({
    "Country": ["USA", "China", "India", "Germany", "Brazil"],
    "GDP": [21000000, 14000000, 2800000, 4000000, 1800000]
})

os.makedirs("data", exist_ok=True)
df_fake.to_csv("data/Countries.csv", index=False)

# ---------------------------
# 2. Init local model
# ---------------------------
model = LocalLLM(
    api_base="http://localhost:11434/v1",
    model="gpt-oss:20b-cloud"
)

# ---------------------------
# 3. SmartDataframe with correct config
# ---------------------------
user_defined_path = "charts/"
sdf = SmartDataframe(
    "data/Countries.csv",
    config={
        "llm": model,
        "enable_cache": False,
        "save_charts": True,
        "save_charts_path": user_defined_path,
        "show_charts": False,  # still set, won't hurt
        "output": "plot"
    }
)

# ---------------------------
# 4. Pre-emptively get current processes
# ---------------------------
before_procs = {p.pid for p in psutil.process_iter()}

# ---------------------------
# 5. Ask for the chart
# ---------------------------
response = sdf.chat(
    "Plot a histogram of the GDP for each country with different bar colors."
)

# ---------------------------
# 6. Kill any new processes that opened chart files
# ---------------------------
time.sleep(0.5)  # small delay to allow OS to spawn viewer
for p in psutil.process_iter(['pid', 'name', 'exe', 'cmdline']):
    if p.info['pid'] not in before_procs:
        name = (p.info['name'] or "").lower()
        cmd = " ".join(p.info['cmdline'] or [])
        # check common image apps / Office apps
        if any(x in name for x in ["photos", "mspaint", "excel", "powerpnt", "chrome"]):
            try:
                p.kill()
                print(f"Killed auto-opened process: {name} ({p.info['pid']})")
            except Exception:
                pass

# Optional: print response
# print("Chat response:", response)

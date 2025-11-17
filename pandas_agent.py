# Install dependencies first (run in terminal):
# pip install pandas matplotlib seaborn pandasai ollama

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pandasai import SmartDataframe
from langchain_ollama import ChatOllama
from langchain_community.llms import Ollama

# -----------------------------
# 1. Load or create a DataFrame
# -----------------------------
# Example dataset
data = {
    "Year": [2020, 2021, 2022, 2023],
    "Sales": [150, 200, 250, 300],
    "Profit": [50, 70, 90, 120]
}
df = pd.DataFrame(data)

# -----------------------------
# 2. Connect to Ollama LLM
# -----------------------------
# Make sure you have Ollama installed and a model pulled, e.g.:
# ollama pull mistral
llm = ChatOllama(model="gpt-oss:20b-cloud")  # You can replace with "llama2", "gemma", etc.
# llm = Ollama(model="qwen3:0.6b")

# -----------------------------
# 3. Wrap DataFrame with PandasAI
# -----------------------------
sdf = SmartDataframe(df, config={"llm": llm})

# -----------------------------
# 4. Ask questions in natural language
# -----------------------------
try:
    print("=== Natural Language Query ===")
    answer = sdf.chat("What is the average profit per year?")
    print("Answer:", answer)

    # Generate a chart
    print("\n=== Generating Chart ===")
    sdf.chat("Plot a line chart of Sales and Profit over Year with proper labels and title.")
    plt.show()

except Exception as e:
    print("Error:", e)

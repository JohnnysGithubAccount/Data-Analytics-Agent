import json
import os

import pandas as pd
from typing import Dict, Any

class DataOverview:
    def __init__(self, llm, data_root=r"D:\UsingSpace\Projects\Artificial Intelligent\Agent\Data Analytics Agent\backend\uploads"):
        """
        llm: your external reasoning model (ChatOllama, GPT, etc.)
        """
        self.llm = llm
        self.data_root = data_root

    def load_dataframe(self, filename: str) -> pd.DataFrame:
        """
        Load a dataframe from a file in DATA_PARENT_DIR.
        Supports CSV and Excel files.
        """
        path = os.path.join(self.data_root, filename)

        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        # File type detection
        ext = filename.lower().split(".")[-1]

        if ext == "csv":
            return pd.read_csv(path)

        elif ext in ["xlsx", "xls"]:
            return pd.read_excel(path)

        else:
            raise ValueError(
                f"Unsupported file format '{ext}'. Only CSV or Excel is allowed."
            )

    def __call__(self, state: Dict[str, Any]) -> Dict[str, Any]:
        print("DATA OVERVIEW")

        df = self.load_dataframe(state['file_name'])

        # ----- Prepare raw info -----
        columns = list(df.columns)
        dtypes = df.dtypes.astype(str).to_dict()
        head = df.head(5).to_dict(orient="records")
        describe = df.describe(include="all").fillna("").to_dict()

        # Build a structured JSON-like snapshot
        raw_profile = {
            "columns": columns,
            "dtypes": dtypes,
            "sample_rows": head,
            "describe": describe,
            "num_rows": len(df),
            "num_columns": len(df.columns)
        }

        # Create overview prompt
        prompt = f"""
            You are a Data Analyst Agent.
            Summarize the dataset based on the structured information below.
            
            Your output should:
            - Be concise but informative.
            - Identify numeric vs categorical fields.
            - Short and compact but have to be greatly informative.
            
            RAW DATA PROFILE (JSON):
            {json.dumps(raw_profile, indent=2)}
            
            Return a natural language summary ONLY.
        """

        overview = self.llm.invoke(prompt)

        # Add to state
        state["overview"] = overview
        # state['df'] = df

        # print(f"[OVERVIEW RESPONSE]")
        # for line in overview.content.splitlines():
        #     print(f"\t[LINE] {line}")

        return state

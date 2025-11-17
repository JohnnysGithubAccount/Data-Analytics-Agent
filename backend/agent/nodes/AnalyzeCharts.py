from dataclasses import dataclass
from typing import Optional, Any, Dict, Annotated, List

from langchain.retrievers import MultiQueryRetriever
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_ollama import ChatOllama
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages
from langchain_core.messages import AnyMessage, AIMessage
from langgraph.graph import StateGraph, END
import base64
import os
from io import BytesIO
from PIL import Image


class ChartAnalyzeAgent:
    def __init__(self, vlm, charts_folder="charts", analysis_folder="analysis"):
        """
        vlm: already initialized ChatOllama object
        """
        self.vlm = vlm
        self.charts_folder = charts_folder
        self.analysis_folder = analysis_folder
        os.makedirs(self.analysis_folder, exist_ok=True)

    def process_image(self, image_path):
        if not os.path.exists(image_path):
            raise FileNotFoundError(f"Image not found: {image_path}")

        with Image.open(image_path) as img:
            # Convert RGBA to RGB if needed
            if img.mode in ("RGBA", "LA") or (img.mode == "P" and "transparency" in img.info):
                img = img.convert("RGB")
            buffered = BytesIO()
            img.save(buffered, format="JPEG")
            img_b64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
        return img_b64

    def analyze_chart(self, chart_path):
        """
        Generates textual analysis for a single chart using the provided vlm.
        """
        image_b64 = self.process_image(chart_path)

        system_prompt = """
        You are a data analyst. You will receive:
        - Some contextual information
        - A chart image

        Your job: provide a deep, professional analysis.
        """
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            MessagesPlaceholder("overview"),
            (
                "human",
                [
                    {
                        "type": "image_url",
                        "image_url": "data:image/jpeg;base64,{image_b64}",
                    },
                    {
                        "type": "text",
                        "text": "{text}"
                    }
                ]
            )
        ])
        # Input dictionary
        inputs = {
            "image_b64": image_b64,
            "text": "What do you see in this image?",
            "overview": [
                AIMessage("Data about app user's account plan registration.")
            ]
        }

        chain = prompt | self.vlm
        response = chain.invoke(inputs)
        return response.content

    def __call__(self, state):
        """
        Loops through all charts and saves analysis to text files.
        Returns structured response.
        """
        print("CHART ANALYZE AGENT")
        chart_files = [f for f in os.listdir(self.charts_folder)
                       if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        for chart_file in chart_files[0:3]:
            chart_path = os.path.join(self.charts_folder, chart_file)
            analysis_text = self.analyze_chart(chart_path)
            # print(f"Done analyzed image: {chart_file}")

            # Save analysis to text file with same name as chart
            analysis_file = os.path.join(
                self.analysis_folder,
                os.path.splitext(chart_file)[0] + ".txt"
            )
            with open(analysis_file, "w", encoding="utf-8") as f:
                f.write(analysis_text)

        return {"agent_responses": [AIMessage(content="Finished analysis on charts by chart_analysis_agent. Moving on to insights_agent.")]}

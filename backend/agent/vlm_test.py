import base64
from io import BytesIO
from PIL import Image
import os

from langchain_core.messages import AIMessage
from langchain_core.prompts import MessagesPlaceholder
from langchain_ollama import ChatOllama
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser

# ---------------------------
# Convert image to Base64
# ---------------------------
def image_to_base64(image_path):
    with Image.open(image_path) as img:
        if img.mode in ("RGBA", "LA"):
            img = img.convert("RGB")
        buf = BytesIO()
        img.save(buf, format="JPEG")
        return base64.b64encode(buf.getvalue()).decode("utf-8")

image_path = r"D:\UsingSpace\Projects\Artificial Intelligent\Agent\Data Analytics Agent\backend\agent\charts\579233df-47ab-45ff-9313-0d5552666f22.png"
image_b64 = image_to_base64(image_path)

# ---------------------------
# Initialize Vision LLM
# ---------------------------
llm = ChatOllama(model="qwen3-vl:235b-cloud", temperature=0)

# ---------------------------
# Build ChatPromptTemplate
# ---------------------------
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

# ---------------------------
# Prepare input values
# ---------------------------
inputs = {
    "image_b64": image_b64,
    "text": "What do you see in this image?",
    "overview": [
        AIMessage("Data about app user's account plan registration.")
    ]
}

# ---------------------------
# Run the chain
# ---------------------------
chain = prompt | llm | StrOutputParser()
response = chain.invoke(inputs)

print("\nAI Response:\n", response)

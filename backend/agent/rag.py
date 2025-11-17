import pandas as pd
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.chat_models import ChatOllama
from langchain.retrievers.multi_query import MultiQueryRetriever
from langchain.prompts import PromptTemplate, ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser


# === 1️⃣ Load Excel and build text ===
excel_path = r"D:\UsingSpace\Projects\Artificial Intelligent\Agent\Data Analytics Agent\backend\uploads\fake_dataset.xlsx"
df = pd.read_excel(excel_path)
data = df.to_string(index=False)

text_splitter = RecursiveCharacterTextSplitter(chunk_size=7500, chunk_overlap=100)
chunks = text_splitter.split_text(data)

# === 2️⃣ Build and persist vector DB ===
embedding_model = OllamaEmbeddings(model="nomic-embed-text", show_progress=False)
persist_dir = "fake_dataset"
collection_name = "fake_dataset"

vector_db = Chroma.from_texts(
    texts=chunks,
    embedding=embedding_model,
    collection_name=collection_name,
    persist_directory=persist_dir,
)
vector_db.persist()

print(f"✅ Vector DB saved to {persist_dir}")

# === 3️⃣ Initialize LLM ===
local_model = "gpt-oss:20b-cloud"
llm = ChatOllama(model=local_model, temperature=.0)

# === 4️⃣ Define MultiQueryRetriever ===
QUERY_PROMPT = PromptTemplate(
    input_variables=["question"],
    template="""You are an AI assistant. Generate multiple diverse queries to retrieve the most relevant data 
    from a table containing columns such as Id, order_id, name, sales, refund, and status.
    Original user question: {question}""",
)

retriever = MultiQueryRetriever.from_llm(
    vector_db.as_retriever(),
    llm,
    prompt=QUERY_PROMPT
)

# === 5️⃣ Define RAG Chain ===
template = """Answer the question based ONLY on the following context:
{context}
Question: {question}
"""

prompt = ChatPromptTemplate.from_template(template)

chain = (
    {"context": retriever, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# === 6️⃣ Ask a question ===
query = "How many rows are there in the dataset?"
print(f"\n🔍 Query: {query}\n")

raw_result = chain.invoke(query)
final_result = f"{raw_result}\n\nIf you have more questions, feel free to ask!"
print("🧠 Final Answer:\n", final_result)

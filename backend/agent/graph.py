from langchain_core.runnables import RunnableConfig
from langchain_neo4j import Neo4jVector
from langgraph.constants import END
from langgraph.graph import StateGraph, START
from langgraph.checkpoint.memory import InMemorySaver
from langchain_ollama import ChatOllama, OllamaEmbeddings

from backend.agent.nodes.DataOverview import DataOverview
from backend.agent.nodes.Manager import Manager
from backend.agent.nodes.PlanAgent import PlanAgent
from backend.agent.nodes.DrawingChart import ChartDrawingAgent
from backend.agent.nodes.AnalyzeCharts import ChartAnalyzeAgent
from backend.agent.nodes.Insights import InsightsAgent
from backend.agent.routers.ManagerRouter import ManagerRouter
from backend.agent.utils import State, plot_graph
from backend.agent.tool import tools_list


# === Init objects ===
members = ["planning_agent", "chart_drawing_agent", "chart_analysis_agent", "insights_agent"]
llm = ChatOllama(
    model="gpt-oss:20b-cloud",
    # model="minimax-m2:cloud",
    temperature=0,
)
vlm = ChatOllama(
    model="qwen3-vl:235b-cloud",
    temperature=0
)

data_overview = DataOverview(llm=llm)
manager_agent = Manager(llm=llm)
planning_agent = PlanAgent(llm=llm)
chart_drawing_agent = ChartDrawingAgent(llm=llm)
chart_analysis_agent = ChartAnalyzeAgent(vlm=vlm)
insights_agent = InsightsAgent(llm=llm)

# === Router ===
router = ManagerRouter()

# === Graph Nodes Definition ===
graph_builder = StateGraph(State)
graph_builder.add_node("data_overview", data_overview)
graph_builder.add_node("manager_agent", manager_agent)
graph_builder.add_node("planning_agent", planning_agent)
graph_builder.add_node("chart_drawing_agent", chart_drawing_agent)
graph_builder.add_node("chart_analysis_agent", chart_analysis_agent)
graph_builder.add_node("insights_agent", insights_agent)

# === Graph Edges Definition ===
graph_builder.add_edge(START, "data_overview")
graph_builder.add_edge("data_overview", "manager_agent")
for member in members:
    graph_builder.add_edge(member, "manager_agent")

# === Conditional edges ===
graph_builder.add_conditional_edges(
    "manager_agent",
    router,
    {
        "planning": "planning_agent",
        "drawing": "chart_drawing_agent",
        "chart_analyze": "chart_analysis_agent",
        "insights": "insights_agent",
        "try_again": "manager_agent",
        "finish": END
    }
)

# === Compile graph ===
memory = InMemorySaver()
graph = graph_builder.compile(
    checkpointer=memory
)

# === Entrypoint ===
def main():
    plot_graph(graph, "graphs/instance.png")

    # === Test pass ===
    config = RunnableConfig(
        run_name="graph_test_run",
        configurable={"thread_id": "test-thread-1"},
        recursion_limit=100
    )

    user_prompt = "How many rows are there?"
    user_prompt = "Here is my data, give me insights on it."
    input_state = {
        "input_prompt": user_prompt,
        "file_name": "fake_dataset.xlsx"
    }
    for step in graph.stream(input_state, config):
        for node_name, output in step.items():
            # print("Node name:", node_name)
            # print(output.get("input_prompt", []))
            # print(output.get("file_name", []))
            # print(output.get("overview", "no overview"))
            # print(output.get("command", "blank command"))
            # print(output.get("next_agent", "bank next agent"))

            # print(f"[INFO] {node_name} RESPONSES:")
            # for response in output.get("agent_responses", []):
                # print(f"\t[RESPONSE] {response}")

            print("=" * 30)


if __name__ == "__main__":
    main()
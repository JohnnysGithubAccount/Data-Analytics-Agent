### 📝 Overview
This project implements an **autonomous data analytics platform** powered by a **multi-agent system**. Each agent specializes in tasks such as **data preprocessing, querying, visualization, and interpretation**, and they collaborate to deliver end-to-end insights with minimal human intervention.

### Backend deployment
Only the frontend is deployed already, the backend will be online soon.

### ✨ Key Features
- 🤝 **Multi-Agent Collaboration**: Agents coordinate using **LangChain** and **LangGraph** to manage workflows.  
- 💬 **Natural Language Interface**: Users can interact with the system conversationally, delegating analytics tasks to agents.  
- 📈 **Data Analysis Automation**: Integration with **PandasAI** enables intelligent handling of tabular datasets.  
- ⚡ **Scalable Backend**: Built with **FastAPI** for efficient API serving and orchestration.  
- 🎨 **Interactive Frontend**: A **ReactJS** interface provides real-time visualization and user-friendly dashboards.  
- 🧠 **LLM Integration**: Powered by **Ollama**, enabling reasoning and contextual understanding across agents.  

### 🛠️ Technologies
- 🔗 **LangChain, LangGraph** – Agent orchestration and workflow management  
- 🧠 **Ollama** – LLM-powered reasoning and decision-making  
- ⚡ **FastAPI** – Backend services and API endpoints  
- 🎨 **ReactJS** – Frontend visualization and interaction  
- 📊 **PandasAI** – Automated data analysis and query execution  

---

### 🧩 System Architecture
<p align="center">
  <img width="784" height="335" alt="image" src="https://github.com/user-attachments/assets/cde05b88-bfd2-4422-9b44-48e657ca6da5" />
</p>

The system is designed as a **modular multi-agent workflow**, orchestrated by a central **Manager Agent** that coordinates specialized agents to perform distinct analytics tasks. This architecture enables scalable, autonomous, and iterative data analysis.

#### 🔄 Agent Workflow Overview
- 🟢 **Start Node (`__start__`)**: Initializes the data analysis pipeline.
- 📊 **Data Overview Agent**: Summarizes and prepares the dataset for processing.
- 🧑‍💼 **Manager Agent**: Central controller that delegates tasks to specialized agents.

#### 🧠 Specialized Agents
- 🗺️ **Planning Agent** (`planning`) – Strategizes analysis steps and selects chart types.
- 📈 **Chart Drawing Agent** (`drawing`) – Generates visualizations based on planning output.
- 🔍 **Chart Analysis Agent** (`chart_analyze`) – Interprets visualizations to extract patterns and insights.
- 💡 **Insights Agent** (`insights`) – Synthesizes findings into human-readable recommendations.

#### 🔁 Iterative Feedback Loop
- 🔁 **Retry Mechanism** (`try_again`) – Loops back from the end node to the Manager Agent for refinement.
- 🛑 **End Node (`__end__`)**: Marks completion of the workflow, with optional retry if needed.

This architecture supports **autonomous, conversational analytics** with minimal human input, ideal for dynamic data environments and real-time decision-making.

### 📊 Result

#### Uploading Interface
<p align="center">
  <img width="1746" height="978" alt="image" src="https://github.com/user-attachments/assets/655a6c36-0f54-4776-ae6b-465de84046bd" />
</p>

The frontend is a sleek, user-friendly web application built with **ReactJS**, designed to streamline the data analysis workflow through intuitive interactions.

- Users can upload **CSV or Excel files** directly through a central "Upload Your Data" panel.
- A **pre-filled instruction box** allows users to describe their dataset and specify analysis goals in natural language.
- Example input:  
  _“Here is my app registration data. It includes users' account, accounts' information, plans and balance. Give me professional insights. And some future direction also.”_
- A prominent **"ANALYZE" button** triggers the multi-agent system to begin processing the uploaded data and generate insights.
- The system interprets user instructions and coordinates agents for planning, visualization, and interpretation.

#### Data preview

- Uploaded **CSV or Excel files** are rendered as interactive tables.
- Users can scroll through rows and columns to inspect raw data directly within the browser.
- Supports **pagination** and **column sorting** for large datasets.

<p align="center">
<img width="1744" height="977" alt="image" src="https://github.com/user-attachments/assets/1a129bd1-7fde-41e1-aa57-acc03f7300c0" />
</p>

#### Workflow tracking

When you hit analyze, a window pops up and show you the multi-agent working. A node will lights up when it's finished.

<p align="center">
<img width="1742" height="980" alt="image" src="https://github.com/user-attachments/assets/e19a1d91-f9ad-4c95-b2f5-35d0be389ff6" />
</p>

#### Analyze result
This tab display charts and their's analysis. Each chart will have its own analysis.

<p align="center">
<img width="1744" height="979" alt="image" src="https://github.com/user-attachments/assets/cd7003fb-7162-4224-a6eb-88db840591ff" />

</p>

#### Insights
The overall insights over your data will be displayed here

<p align="center">
<img width="1744" height="979" alt="image" src="https://github.com/user-attachments/assets/30ca5a95-b29a-4188-a49d-a90d56533860" />

</p>

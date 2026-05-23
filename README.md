# Agentic AI LangGraph Tutorials 🤖🦜🔗

A comprehensive, hands-on tutorial series teaching **LangGraph 1.1.9** from beginner to expert level. Build stateful, multi-actor LLM applications, parallel subgraphs, human-in-the-loop workflows, supervisor/swarm multi-agent networks, and production-grade architectures. All tutorials are powered by **NVIDIA NIM** (free tier) — no paid API keys required.

---

## 🔒 Secure Secret Management & Environment Configuration

To keep agentic applications secure and production-ready, **never hardcode API keys, credentials, or sensitive configurations** in your source files or notebooks.

All notebooks in this repository are pre-configured to load variables from a local `.env` environment file securely and override any stale in-memory variables.

### 1. Configure Your Secrets File
Copy the provided `.env.example` file to `.env`:
```bash
cp .env.example .env
```
Open `.env` and fill in your keys:
```ini
# NVIDIA NIM API Key (Get a free key at build.nvidia.com)
NVIDIA_API_KEY=nvapi-your-key-here

# LangSmith Observability Keys (Optional, required for Notebook 10)
LANGSMITH_API_KEY=ls-your-key-here
LANGCHAIN_TRACING_V2=true
LANGCHAIN_PROJECT=langgraph-tutorials

# Optional: Tavily Search API Key (tavily.com)
TAVILY_API_KEY=your-tavily-key-here
```

### 2. Standard Secure Loading Pattern in Jupyter Notebooks
To ensure the notebook always uses the active key in your `.env` and ignores stale cached variables in Jupyter's memory, use the `python-dotenv` package with the `override=True` modifier:

```python
import os
import certifi
from dotenv import load_dotenv

# Force load and overwrite cached environment variables
load_dotenv(override=True)

# Securely bind the active TLS CA bundle path dynamically (fixes OSError cert issues)
os.environ['REQUESTS_CA_BUNDLE'] = certifi.where()
os.environ['SSL_CERT_FILE'] = certifi.where()

# Access keys securely
nvidia_api_key = os.getenv("NVIDIA_API_KEY")
if not nvidia_api_key or nvidia_api_key == "nvapi-your-key-here":
    raise ValueError("❌ NVIDIA_API_KEY is missing! Please configure it in your .env file.")
```

---

## 🚀 Quick Start

### 1. Clone the Repository & Setup Environment
Make sure you have **Python 3.12+** installed, then follow the instructions for your preferred installation method below:

#### Option A: Standard `venv` & `pip` (Easiest & Most Compatible)
This method uses Python's built-in virtual environment library and the standard `pip` installer.

1. **Clone the Repository & Navigate In:**
   ```bash
   git clone https://github.com/aashishgarg13/Agentic-AI-langraph-tutorials.git
   cd Agentic-AI-langraph-tutorials
   ```

2. **Create and Activate the Virtual Environment:**
   * **macOS / Linux:**
     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     ```
   * **Windows (PowerShell):**
     ```powershell
     python -m venv .venv
     .venv\Scripts\Activate.ps1
     ```
   * **Windows (Command Prompt / cmd.exe):**
     ```cmd
     python -m venv .venv
     .venv\Scripts\activate.bat
     ```

3. **Upgrade pip & Install All Dependencies:**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt
   ```

---

#### Option B: Ultra-Fast `uv` Package Manager (Recommended for Speed)
If you have the ultra-fast Python package installer `uv` installed, use this method.

1. **Clone the Repository & Navigate In:**
   ```bash
   git clone https://github.com/aashishgarg13/Agentic-AI-langraph-tutorials.git
   cd Agentic-AI-langraph-tutorials
   ```

2. **Create and Activate the Virtual Environment using `uv`:**
   * **macOS / Linux:**
     ```bash
     uv venv --python 3.12
     source .venv/bin/activate
     ```
   * **Windows (PowerShell):**
     ```powershell
     uv venv --python 3.12
     .venv\Scripts\Activate.ps1
     ```
   * **Windows (Command Prompt / cmd.exe):**
     ```cmd
     uv venv --python 3.12
     .venv\Scripts\activate.bat
     ```

3. **Install All Dependencies:**
   ```bash
   uv pip install -r requirements.txt
   ```


### 2. Register Jupyter Kernel (CRITICAL to avoid ModuleNotFound errors)
If you launch Jupyter globally, it might not automatically use your active virtual environment. To prevent `ModuleNotFoundError: No module named 'langgraph.checkpoint.sqlite'`, register your virtual environment kernel with Jupyter:
```bash
# Ensure you are inside the active virtual environment, then run:
python -m ipykernel install --user --name=langgraph-tutorials --display-name "Python (langgraph-tutorials)"
```
When opening any notebook in Jupyter, make sure to select the **Python (langgraph-tutorials)** kernel from the top-right Kernel selector.

### 3. Get Your Free NVIDIA NIM Key
1. Sign up for a free developer account at [build.nvidia.com](https://build.nvidia.com/).
2. Select any LLM page (e.g., [Llama 3.3 70B](https://build.nvidia.com/meta/llama-3_3-70b-instruct)).
3. Click **"Get API Key"** and copy the token starting with `nvapi-...`.
4. Add it to your local `.env` file.

### 4. Launch Jupyter
```bash
jupyter notebook
```


---

## 📓 Notebooks Curriculum & Quick-Tutorial

All notebooks are organized into a logical 10-step sequential curriculum:

### 1. LangGraph Fundamentals & Core Features
| # | Topic | Key Concept | File Link |
|---|---|---|---|
| **01** | Introduction to LangGraph | StateGraph, Nodes, Edges, State Merging | [01_introduction_to_langgraph.ipynb](01_introduction_to_langgraph.ipynb) |
| **02** | Conditional Routing | Conditional edges, loop limits, Command-based routing | [02_conditional_routing.ipynb](02_conditional_routing.ipynb) |
| **03** | Tool Integration & Agents | Bind tools, ReAct agent loop, tool execution nodes | [03_tool_integration_openai.ipynb](03_tool_integration_openai.ipynb) |
| **04** | State Persistence & Memory | Thread-id checkpointing, SqliteSaver session state | [04_state_persistence_and_memory.ipynb](04_state_persistence_and_memory.ipynb) |
| **05** | Human-in-the-Loop & Resumption | Dynamic interrupts, approval gates, Command resumption | [05_human_in_the_loop_streaming.ipynb](05_human_in_the_loop_streaming.ipynb) |

### 2. Advanced Graph Architectures & Patterns
| # | Topic | Key Concept | File Link |
|---|---|---|---|
| **06** | Parallel Execution & Subgraphs | Parallel Fan-out/Fan-in, breakout Command.PARENT | [06_parallel_execution_subgraphs.ipynb](06_parallel_execution_subgraphs.ipynb) |
| **07** | Production Patterns | State controllers, error-handling retry branches, fallbacks | [07_production_patterns_advanced_features.ipynb](07_production_patterns_advanced_features.ipynb) |
| **08** | Functional API & Stores | `@entrypoint`, `@task` decorators, cross-session Stores | [08_command_functional_api_longterm_memory.ipynb](08_command_functional_api_longterm_memory.ipynb) |

### 3. Multi-Agent Networks & Platform Tooling
| # | Topic | Key Concept | File Link |
|---|---|---|---|
| **09** | Multi-Agent Systems | Supervisor orchestration, Swarm handoffs, transfer tools | [09_multi_agent_systems.ipynb](09_multi_agent_systems.ipynb) |
| **10** | Observability & Testing | Unit testing graphs, LangGraph SDK & Platform CLI | [10_testing_observability_platform.ipynb](10_testing_observability_platform.ipynb) |

---

## 📖 Quick Tutorial: Core Concepts & Python Code Patterns

### Module 1: LangGraph Fundamentals & Core Features

#### 01. Introduction to LangGraph
* **Concept**: Build stateful agent applications structured as graphs. The **State** is a shared data structure passed between **Nodes** (Python functions that process and return state updates) connected by **Edges** (execution paths).
* **Code Pattern**:
  ```python
  from langgraph.graph import StateGraph, START, END
  from typing_extensions import TypedDict

  class State(TypedDict):
      text: str

  def node_a(state: State) -> dict:
      return {"text": state["text"] + "a"}

  builder = StateGraph(State)
  builder.add_node("node_a", node_a)
  builder.add_edge(START, "node_a")
  builder.add_edge("node_a", END)
  graph = builder.compile()
  ```

#### 02. Conditional Routing & Command routing
* **Concept**: Dynamically route graph execution. While traditional setups use `add_conditional_edges` and separate routers, LangGraph's modern **`Command`** class allows a node to execute state updates and declare the next destination (`goto`) in a single return, avoiding double computations.
* **Code Pattern**:
  ```python
  from langgraph.types import Command

  def analyze_and_route(state: State) -> Command:
      score = len(state["text"]) / 100
      destination = "approve" if score >= 0.7 else "reject"
      return Command(update={"score": score}, goto=destination)
  ```

#### 03. Tool Integration & Agents
* **Concept**: Integrate external tools into your agents. We bind tools to `ChatNVIDIA` using `.bind_tools()` and run a compiled graph with the prebuilt `ToolNode` to execute tools whenever the LLM requests a function call.
* **Code Pattern**:
  ```python
  from langchain_nvidia_ai_endpoints import ChatNVIDIA
  from langgraph.prebuilt import ToolNode, tools_condition

  llm = ChatNVIDIA(model="meta/llama-3.3-70b-instruct").bind_tools([get_weather])
  tool_node = ToolNode([get_weather])

  # In graph builder:
  # builder.add_conditional_edges("agent", tools_condition)
  ```

#### 04. State Persistence & Memory
* **Concept**: Short-term conversation persistence. Thread checkpointing allows the graph to automatically save and retrieve states between turns. Adding a checkpointer (like `SqliteSaver`) creates native session memory.
* **Code Pattern**:
  ```python
  from langgraph.checkpoint.sqlite import SqliteSaver
  import sqlite3

  db = sqlite3.connect(":memory:", check_same_thread=False)
  memory = SqliteSaver(db)
  graph = builder.compile(checkpointer=memory)

  # Invoke with thread config
  config = {"configurable": {"thread_id": "session-123"}}
  graph.invoke(input_state, config)
  ```

#### 05. Human-in-the-Loop & Resumption
* **Concept**: Pause graphs for human verification. In LangGraph 1.1.9, the canonical pattern calls the `interrupt()` primitive inside the node, suspending execution. The user can then resume execution by sending a `Command(resume=...)` response.
* **Code Pattern**:
  ```python
  from langgraph.types import interrupt, Command

  def review_gate(state: State) -> Command:
      # Pauses execution and returns payload to user
      decision = interrupt({"content": state["content"], "action": "Approve?"})
      return Command(update={"approved": decision == "yes"}, goto="publish" if decision == "yes" else "reject")

  # Resume later in external code:
  graph.invoke(Command(resume="yes"), config)
  ```

---

### Module 2: Advanced Graph Architectures & Patterns

#### 06. Parallel Execution & Subgraphs
* **Concept**: Optimize workflows by running independent operations in parallel (Fan-out/Fan-in) and structuring complex systems as nested subgraphs. A subgraph node can break out and dynamically route inside a parent graph using `Command(graph=Command.PARENT)`.
* **Code Pattern**:
  ```python
  # Parallel Edge Setup
  builder.add_edge("prepare", "parallel_node_1")
  builder.add_edge("prepare", "parallel_node_2")
  builder.add_edge("parallel_node_1", "merge")
  builder.add_edge("parallel_node_2", "merge")
  ```

#### 07. Production Patterns
* **Concept**: Building robust, fault-tolerant enterprise graphs. Implements validation gates, schema state reducers, fallback execution branches, and robust try-except error handlers that route exceptions safely back to retry or notification nodes.
* **Code Pattern**:
  ```python
  def execute_task(state: State) -> Command:
      try:
          result = call_flaky_service()
          return Command(update={"result": result}, goto="success_node")
      except Exception as e:
          return Command(update={"error": str(e)}, goto="error_handler")
  ```

#### 08. Functional API & Long-Term Memory (Stores)
* **Concept**: 
  1. **Functional API**: Write stateful workflows as standard Python functions using `@entrypoint` and `@task` decorators, bypassing explicit graph creation.
  2. **Stores**: Persistent, cross-thread, long-term memory. Unlike checkpointers (which are locked to a single thread), Stores (`InMemoryStore`, `PostgresStore`) store data across all threads and user sessions.
* **Code Pattern**:
  ```python
  from langgraph.func import entrypoint, task
  from langgraph.store.memory import InMemoryStore

  store = InMemoryStore()

  @task
  def extract_facts(text: str) -> str:
      return "User prefers Python."

  @entrypoint(checkpointer=MemorySaver(), store=store)
  def assistant_workflow(query: str, *, store) -> str:
      # Retrieve long-term preferences across sessions
      memories = store.search(("users", "alice"))
      return "Answer based on context and memories"
  ```

---

### Module 3: Multi-Agent Networks & Platform Tooling

#### 09. Multi-Agent Systems (Supervisor & Swarms)
* **Concept**: Coordinate multiple specialized AI actors:
  * **Supervisor**: A central manager LLM receives user inputs and dynamically delegates tasks to workers via `langgraph-supervisor`.
  * **Swarm**: A collaborative model where independent agents hand off control to other agents dynamically via handoff tools (`langgraph-swarm`).
* **Code Pattern**:
  ```python
  from langgraph_supervisor import create_supervisor
  
  # Supervisor pattern automatically orchestrates dynamic dispatching
  supervisor = create_supervisor([writer_agent, researcher_agent], model=llm)
  app = supervisor.compile()
  ```

#### 10. Testing, Observability & LangGraph Platform
* **Concept**: Transitioning agents from Jupyter to production. Track and evaluate agent traces in real time with OpenTelemetry-compliant observability engines (Opik/LangSmith). Deploy workflows to cloud platforms with Docker, CLI, and SDK clients.
* **Code Pattern**:
  ```python
  # Configure environment variables for full tracing:
  os.environ["LANGCHAIN_TRACING_V2"] = "true"
  os.environ["LANGCHAIN_PROJECT"] = "agent-unit-tests"
  ```

---

## 🛠 Technology Stack

* **LangGraph** — Complex stateful graph architectures & workflows (StateGraph, Command, Functional API)
* **NVIDIA NIM** — Fast, free-tier hosted inference endpoints (`ChatNVIDIA`)
* **LangChain Core** — Underlying base model, prompt, and tool interfaces
* **Opik / LangSmith** — Production-grade LLM observability, trace monitoring, and dataset testing
* **uv & Hatchling** — High-performance python packaging and virtual environment management

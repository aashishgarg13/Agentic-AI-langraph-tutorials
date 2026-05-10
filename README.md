# LangGraph Tutorial Series — Powered by NVIDIA NIM 🚀

A comprehensive, hands-on tutorial series teaching **LangGraph 1.1.9** from beginner to advanced level. All notebooks run on **NVIDIA NIM** (free tier) — no paid API keys required.

## 🟢 Free to Run — NVIDIA NIM

This entire tutorial series uses **NVIDIA NIM** inference endpoints, which offer a **free tier** with generous daily limits. Unlike OpenAI or Anthropic APIs, you can complete all 10 notebooks **at zero cost**.

### How it works

| | Details |
|---|---|
| **Provider** | [NVIDIA NIM](https://build.nvidia.com/) — hosted inference for open-source models |
| **Models used** | `meta/llama-3.3-70b-instruct` (complex reasoning) · `meta/llama-3.1-8b-instruct` (fast tasks) |
| **Cost** | **Free** — NVIDIA provides a free-tier API key with daily rate limits |
| **Rate limits** | The free tier has usage caps. All notebooks include a built-in `_invoke_with_backoff()` helper that automatically retries with exponential backoff on 429 (rate-limit) errors |
| **API key** | Get yours in 30 seconds at [build.nvidia.com](https://build.nvidia.com/) — no credit card needed |

> **💡 Tip:** If you hit rate limits frequently, add `time.sleep(5)` between cell executions, or run notebooks across multiple sessions.

---

## Overview

LangGraph is a powerful framework for building stateful, multi-actor applications with LLMs. This tutorial series takes you from basic graph construction to building production-ready, multi-agent systems.

## What You'll Learn

By completing this series, you will be able to:

- Build stateful workflows with LangGraph's StateGraph API
- Integrate LLMs with tool/function calling via NVIDIA NIM
- Implement conversation memory and persistence
- Create human-in-the-loop approval workflows
- Design multi-agent systems with parallel execution
- Apply production-ready patterns and optimizations
- Deploy LangGraph applications with confidence

## Tutorial Structure

| Notebook | Topic | Level | Time |
|---|---|---|---|
| 01 | [Introduction to LangGraph](01_introduction_to_langgraph.ipynb) | Beginner | 30-40 min |
| 02 | [Conditional Routing](02_conditional_routing.ipynb) | Beginner-Int | 30-40 min |
| 03 | [Tool Integration & Agents](03_tool_integration_openai.ipynb) | Intermediate | 45-60 min |
| 04 | [State Persistence & Memory](04_state_persistence_and_memory.ipynb) | Intermediate | 45-60 min |
| 05 | [Human-in-the-Loop & Streaming](05_human_in_the_loop_streaming.ipynb) | Advanced | 50-65 min |
| 06 | [Parallel Execution & Subgraphs](06_parallel_execution_subgraphs.ipynb) | Advanced | 50-65 min |
| 07 | [Production Patterns](07_production_patterns_advanced_features.ipynb) | Advanced | 50-65 min |
| 08 | [Command Primitive, Functional API & Long-Term Memory](08_command_functional_api_longterm_memory.ipynb) | Expert | 60-75 min |
| 09 | [Multi-Agent Systems](09_multi_agent_systems.ipynb) | Expert | 60-75 min |
| 10 | [Testing, Observability & LangGraph Platform](10_testing_observability_platform.ipynb) | Expert | 45-60 min |

## Prerequisites

### Required
- **Python 3.12+** installed
- **uv** package manager ([install instructions](https://github.com/astral-sh/uv))
- Basic to intermediate Python programming skills
- Familiarity with Jupyter Notebooks

### Helpful (but not required)
- Basic understanding of Large Language Models (LLMs)
- Experience with APIs
- Familiarity with async programming in Python

## Setup Instructions

### 1. Clone & Install

```bash
# Clone the repo
git clone https://github.com/aashishgarg13/langraph-tutorials.git
cd langraph-tutorials

# Create virtual environment
uv venv --python 3.12
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows

# Install all dependencies
uv pip install -e .

# Start Jupyter
jupyter notebook
```

### 2. Get Your Free NVIDIA NIM API Key

1. Go to [build.nvidia.com](https://build.nvidia.com/)
2. Sign up or log in (free account, no credit card)
3. Navigate to any model page (e.g., [Llama 3.3 70B](https://build.nvidia.com/meta/llama-3_3-70b-instruct))
4. Click **"Get API Key"** → copy the key (starts with `nvapi-...`)

### 3. Configure Environment

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env and add your NVIDIA API key
# NVIDIA_API_KEY=nvapi-your-key-here
```

> **⚠️ Important:** Never commit your `.env` file. It is already in `.gitignore`.

## Rate Limiting & Free Tier

NVIDIA NIM's free tier has daily rate limits. This tutorial handles them gracefully:

- **Built-in retry logic** — Every notebook includes `_invoke_with_backoff()` which catches 429 errors and retries with exponential backoff (5s → 10s → 20s → 40s)
- **Delays between calls** — Sequential LLM calls include `time.sleep()` pauses to stay within limits
- **Simplified queries** — Complex multi-tool queries are simplified to work reliably with open-source models

If you exhaust your daily limit:
- Wait 24 hours for the limit to reset
- Or generate a new free API key at [build.nvidia.com](https://build.nvidia.com/)

## Learning Path

### For Complete Beginners
Start with Notebook 01 and work through sequentially. Each notebook builds on previous concepts.

### For Developers with LLM Experience
Skim Notebooks 01-02 and start deeper engagement from Notebook 03 onwards.

### For Experienced AI Developers
Review Notebooks 01-04 quickly, then focus on Notebooks 05-07 for advanced patterns.

## Projects Included

- **Notebook 03**: Weather Agent & Math Agent with tool calling
- **Notebook 04**: Customer Support Bot with persistent memory
- **Notebook 05**: Research Assistant with human-in-the-loop
- **Notebook 06**: Multi-Agent Research System with parallel processing
- **Notebook 07**: Enterprise Customer Support System (capstone project)

## Troubleshooting

### API Key / Authentication Errors

```
Exception: [403] Forbidden — Authorization failed
```

- Your API key is expired or invalid
- Generate a new one at [build.nvidia.com](https://build.nvidia.com/)
- Update your `.env` file and **restart the Jupyter kernel**

### Rate Limit Errors (429)

```
⏳ Rate limited — retrying in 5s...
```

This is normal on the free tier. The backoff helper handles it automatically. If it persists after max retries, wait a few minutes and re-run the cell.

### Import Errors

```bash
# Ensure you're in the virtual environment
source .venv/bin/activate

# Reinstall dependencies
uv pip install -e .
```

### Version Compatibility

```bash
python --version       # Should be 3.12+
uv pip show langgraph  # Should be 1.1.9+
```

## Migration Script

The repository includes `migrate_to_nvidia.py` which automates the full migration from OpenAI to NVIDIA NIM:

```bash
python migrate_to_nvidia.py
```

This script:
- Replaces `ChatOpenAI` → `ChatNVIDIA` across all notebooks
- Maps OpenAI model names to NVIDIA equivalents
- Updates environment variable references
- Creates `.env` and `.env.example` files

## Additional Resources

- [LangGraph Official Documentation](https://langchain-ai.github.io/langgraph/)
- [NVIDIA NIM Documentation](https://docs.nvidia.com/nim/)
- [NVIDIA Build Portal](https://build.nvidia.com/)
- [LangChain NVIDIA Integration](https://python.langchain.com/docs/integrations/chat/nvidia_ai_endpoints/)

## Version History

- **v3.0** (May 2026) - NVIDIA NIM Migration
  - Migrated all 10 notebooks from OpenAI to **NVIDIA NIM (free tier)**
  - Models: `meta/llama-3.3-70b-instruct` + `meta/llama-3.1-8b-instruct`
  - Added exponential backoff retry logic for rate limiting
  - Added `migrate_to_nvidia.py` automation script
  - No paid API keys required — fully free to run

- **v2.0** (April 2026) - Major update
  - Expanded to 10 comprehensive notebooks
  - Compatible with LangGraph 1.1.9
  - Migrated to uv + pyproject.toml for package management

- **v1.0** (December 2025) - Initial release
  - 7 comprehensive notebooks
  - Compatible with LangGraph 1.0.5

---

**Ready to start?** Open [Notebook 01: Introduction to LangGraph](01_introduction_to_langgraph.ipynb) and begin your journey into agentic AI! 🚀

# Agentic AI Patterns: From Scratch 🤖

A comprehensive, step-by-step guide to mastering Agentic AI design patterns. This repository builds everything from "raw" Python code to understand the core mechanics of AI agents, avoiding heavy frameworks until the concepts are mastered.

## Stack
- **Language**: Python
- **Model**: Ollama (Llama 3) — OpenAI Compatible SDK

## Curriculum

### Level 1: Foundations (The Basics)
*Focus: Understanding the raw LLM interface.*
1.  **[The Prompt Loop](01_foundations/01_simple_chat)**: Managing conversation history and context windows.
2.  **Structured Output**: Forcing valid JSON for reliable parsing.
3.  **Simple Tool Use**: The mechanics of function calling.

### Level 2: Workflows (Cognitive Architectures)
*Focus: Reliability and Reasoning.*
1.  **Chain of Thought (CoT)**: Explicit reasoning steps.
2.  **ReAct**: The Reason+Act loop for autonomy.
3.  **RAG**: Grounding answers in external data.

### Level 3: Systems (Multi-Agent)
*Focus: Collaboration and Scale.*
1.  **Routing & Classification**: Intent detection.
2.  **Orchestrator-Workers**: Parallel task delegation.
3.  **Evaluator-Optimizer**: Self-improving loops.

## Getting Started

1.  **Install Ollama**:
    Download and install from [ollama.com](https://ollama.com/).

2.  **Pull Llama 3**:
    ```bash
    ollama pull llama3
    ```

3.  **Clone the repo**:
    ```bash
    git clone <your-repo-url>
    cd agentic_ai_patterns
    ```

4.  **Install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```

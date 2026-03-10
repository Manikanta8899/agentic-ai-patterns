# Level 1.3: Simple Tool Use 🛠️

In this lesson, we explore how to give an LLM "tools" (Python functions) that it can decide to call. This is the foundation of autonomous agents.

## Core Concepts

1.  **Tool Definition**: Providing the LLM with a list of available functions, described using JSON Schema.
2.  **Tool Call**: The LLM returns a specific `tool_calls` object instead of a text response, indicating which function to run and with what arguments.
3.  **Local Execution**: YOUR code receives the tool call, executes the actual Python function, and gets a result.
4.  **Tool Response**: You send the function result back to the LLM so it can incorporate that data into its final answer.

## The Tool-Call Lifecycle

1.  **User**: "What's the weather in London?"
2.  **LLM**: (Sees the `get_weather` tool) -> Returns `tool_call: get_weather(location="London")`.
3.  **You**: Executes `get_weather("London")` locally -> Returns `"Sunny, 22°C"`.
4.  **You**: Sends `"Sunny, 22°C"` back to LLM.
5.  **LLM**: "The weather in London is currently sunny and 22°C."

## How to Run

1.  Ensure Ollama is running with `llama3`.
2.  Run the script:
    ```bash
    python tool_use.py
    ```

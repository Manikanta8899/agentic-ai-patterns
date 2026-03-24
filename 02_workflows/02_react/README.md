# Level 2.2: ReAct Pattern (Reason + Act) 🛠️🧠

In this lesson, we move beyond simple reasoning and simple tool use to create **Autonomous Agents** using the **ReAct** pattern.

## What is ReAct?

**ReAct** stands for **Reason + Act**. It is a cognitive architecture where the LLM is prompted to alternate between thinking about a task and performing an action (using a tool).

The cycle looks like this:
1.  **Thought**: The model reasons about the current state and what it needs to do next.
2.  **Action**: The model calls a specific function/tool.
3.  **Observation**: The output of the tool is fed back into the model.
4.  **Repeat**: The model observes the result and updates its "Thought" until it can provide a "Final Answer."

## Why ReAct?

-   **Synergy**: Reasoning helps the model choose the right tools and handle edge cases, while acting provides grounded data that simple reasoning (like CoT) cannot access.
-   **Autonomy**: The agent can navigate multi-step problems that require information retrieval and computation without human interference.
-   **Traceability**: You can follow the agent's exact logic as it navigates the problem.

## How to Run

1.  Ensure Ollama is running with `llama3.2`.
2.  Run the script:
    ```bash
    python react.py
    ```

Observe how the agent first "thinks" about getting the temperature, then "thinks" about calculating the square root of the result it just received!

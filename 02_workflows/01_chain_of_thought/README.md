# Level 2.1: Chain of Thought (CoT) 🧠

In this lesson, we introduce **Workflows**, starting with the widely used **Chain of Thought (CoT)** prompting strategy.

## What is Chain of Thought?

Chain of Thought is a technique where you enforce the LLM to write out its step-by-step reasoning process *before* delivering the final answer. 

Instead of jumping straight from the prompt to the answer (which often leads to hallucination or logical errors in complex tasks), the LLM uses its generation process as a "scratchpad" to compute intermediate steps.

## Core Concepts

1.  **Zero-Shot CoT**: Simply adding "Think step by step" to the prompt or instructing the model to output reasoning before the final answer.
2.  **Few-Shot CoT**: Providing examples of the reasoning process in the prompt to condition the model on how to think.
3.  **Structured Reasoning**: Forcing the model to use XML tags like `<thinking>` and `<answer>`, making it easy for your application to parse the thought process separately from the final result.

## Why use CoT?

-   **Accuracy**: Drastically improves performance on math, logic, and multi-step reasoning tasks.
-   **Debugging / Interpretability**: You can see *why* the model arrived at a specific conclusion.
-   **Agentic Behavior**: It is the foundation for autonomous agents (which need to explicitly reason about what tools to use next).

## How to Run

1.  Make sure Ollama is running with the `llama3.2` model.
2.  Run the script:
    ```bash
    python cot.py
    ```

You will see the difference between a direct prompt (which might guess or be unexplainable) and a CoT prompt (which lays out the logic before concluding).

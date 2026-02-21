# 01. The Prompt Loop (Simple Chat)

This is the "Hello World" of Agentic AI. Before we build complex agents, we must understand the fundamental loop of interaction with a Large Language Model (LLM).

## Key Concepts

1.  **State Management**: LLMs are stateless. They don't remember what you said 5 seconds ago. To create a "conversation", we must send the entire conversation history back to the model with every new message.
    *   In our code, we maintain a `history` list and manually append both user and assistant messages to it.
2.  **Streaming**: Large responses take time. Streaming allows us to show chunks of text as they arrive, creating a responsive feel.
3.  **Local Models**: Using Ollama, we can run powerful LLMs (like Llama 3) entirely on our machine — no API keys, no rate limits, no cost!

## Prerequisites

- [Ollama](https://ollama.com/) installed and running
- `llama3` model pulled: `ollama pull llama3`

## The Code

See `chat.py` for the implementation. Note how we:
1.  Connect to Ollama's local OpenAI-compatible API.
2.  Maintain a `history` list of messages.
3.  Enter a `while True` loop.
4.  Append each user message to history before sending.
5.  Send the **entire** history to get context-aware responses.
6.  Append the assistant's response back to history.

## How to Run

1.  Make sure Ollama is running (`ollama serve` or via the Ollama app).
2.  Activate the virtual environment:
    ```bash
    source venv/bin/activate
    ```
3.  Run the script:
    ```bash
    python 01_foundations/01_simple_chat/chat.py
    ```

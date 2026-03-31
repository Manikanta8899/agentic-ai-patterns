# Level 2.3: RAG (Retrieval Augmented Generation) 📚

In this lesson, we build a complete **RAG pipeline from scratch** — no vector database frameworks, just pure Python and `numpy`.

## What is RAG?

**Retrieval Augmented Generation** is a pattern where you enhance an LLM's response by first **retrieving** relevant documents from a knowledge base and then **injecting** them into the prompt as context. This grounds the model's answer in real data instead of relying on its training knowledge (which may be outdated or missing).

## The RAG Pipeline

```
User Query
    │
    ▼
┌──────────┐     ┌──────────────┐     ┌──────────┐
│  Embed   │────▶│  Similarity  │────▶│ Retrieve │
│  Query   │     │   Search     │     │  Top-K   │
└──────────┘     └──────────────┘     └──────────┘
                                           │
                                           ▼
                                  ┌─────────────────┐
                                  │  LLM + Context   │
                                  │  = Grounded      │
                                  │    Answer         │
                                  └─────────────────┘
```

## Core Concepts

1.  **Document Loading & Chunking**: Splitting large documents into smaller, semantically meaningful chunks.
2.  **Embeddings**: Converting text into numerical vectors that capture meaning, using `nomic-embed-text` via Ollama.
3.  **Cosine Similarity**: A mathematical measure of how "close" two vectors are — used to find chunks most relevant to the user query.
4.  **Context Injection**: Feeding retrieved chunks into the LLM's system prompt so it can answer based on facts, not guesses.

## Prerequisites

You need the `nomic-embed-text` embedding model pulled in Ollama:
```bash
ollama pull nomic-embed-text
```

## How to Run

1.  Ensure Ollama is running with `llama3.2` and `nomic-embed-text`.
2.  Run the script:
    ```bash
    python rag.py
    ```

You'll see the pipeline load documents, create embeddings, retrieve relevant chunks, and then compare a **grounded RAG answer** vs. an **ungrounded answer** (without context).

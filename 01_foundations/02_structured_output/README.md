# 02. Structured Output (JSON Mode)

One of the biggest challenges with LLMs is their tendency to be "chatty." When building agents, we often need the model to return data in a machine-readable format like JSON, not a conversational response.

## Key Concepts

1.  **JSON Mode**: Many modern LLM servers (like Ollama and OpenAI) support a specific "JSON Mode." When enabled, the model is forced to generate a valid JSON string.
2.  **Schema Enforcement**: While JSON mode ensures the *syntax* is correct, it doesn't guarantee the *fields* are what you expect. This is where **Pydantic** comes in.
3.  **Extraction**: Converting unstructured text (like a paragraph) into structured data (like a Python object).

## How it works

1.  **Define a Model**: Create a Pydantic class that defines exactly what fields you want.
2.  **Prompting**: Instruct the model to return ONLY JSON.
3.  **API Call**: Set `response_format={"type": "json_object"}` in the API call.
4.  **Validation**: Pass the resulting string into your Pydantic model. If it fails, you know the data is invalid.

## The Code

See `structured_data.py` for the implementation. We demonstrate how to:
1.  Define a schema for a user profile.
2.  Pass that schema's JSON description to the model.
3.  Parse the model's output safely into a Python object.

## How to Run

1.  Ensure Ollama is running.
2.  Run the script:
    ```bash
    python 01_foundations/02_structured_output/structured_data.py
    ```

import os
from openai import OpenAI
from termcolor import colored

# 1. Configure the Ollama Client
# Ollama exposes an OpenAI-compatible API locally on port 11434.
# No API key needed — everything runs on your machine!
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"  # Ollama doesn't need a real key, but the SDK requires one
)

# 2. Model Selection
# Using the locally installed Llama 3 model via Ollama
MODEL_ID = "llama3"

def main():
    print(colored("🤖 Agentic AI - Level 1: The Prompt Loop", "cyan", attrs=["bold"]))
    print(colored(f"Using local model: {MODEL_ID} (via Ollama)", "cyan"))
    print(colored("Type 'quit' or 'exit' to end the session.\n", "cyan"))

    # 3. Initialize Chat History
    # LLMs are stateless. To create a "conversation", we must send
    # the entire conversation history back with every new message.
    # This is the fundamental concept of the Prompt Loop.
    history = []

    while True:
        try:
            # 4. Get User Input
            user_input = input(colored("You: ", "green"))
            
            if user_input.lower() in ["quit", "exit"]:
                print(colored("\nGoodbye! 👋", "cyan"))
                break
            
            if not user_input.strip():
                continue

            # 5. Append User Message to History
            history.append({"role": "user", "content": user_input})

            # 6. Send the ENTIRE History to the Model (Streamed)
            # Notice: we send the full `history` list every time.
            # This is how the model "remembers" the conversation.
            response = client.chat.completions.create(
                model=MODEL_ID,
                messages=history,
                stream=True
            )

            # 7. Print the Response (Streamed)
            print(colored("Bot: ", "blue"), end="", flush=True)
            full_response = ""
            for chunk in response:
                if chunk.choices[0].delta.content:
                    text = chunk.choices[0].delta.content
                    print(text, end="", flush=True)
                    full_response += text
            print("\n")  # Newline after full response

            # 8. Append Assistant Response to History
            # This completes the loop — both user and assistant messages
            # are now in the history for the next turn.
            history.append({"role": "assistant", "content": full_response})

        except KeyboardInterrupt:
            print(colored("\n\nGoodbye! 👋", "cyan"))
            break
        except Exception as e:
            print(colored(f"\nAn error occurred: {e}", "red"))

if __name__ == "__main__":
    main()

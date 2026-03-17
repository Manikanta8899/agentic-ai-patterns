import os
import json
from openai import OpenAI
from termcolor import colored

# 1. Initialize Client
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)
MODEL_ID = "llama3.2"

def main():
    print(colored("🧠 Agentic AI - Level 2: Workflows - Chain of Thought (CoT)", "cyan", attrs=["bold"]))
    
    # A tricky math/logic word problem
    text_prompt = (
        "Roger has 5 tennis balls. He buys 2 more cans of tennis balls. "
        "Each can has 3 tennis balls. How many tennis balls does he have now?"
    )
    
    print(colored("\n--- Prompt ---", "yellow"))
    print(text_prompt)

    # 1. Direct Prompting (No CoT)
    print(colored("\n--- 1. Direct Prompting (Forced final answer only) ---", "blue", attrs=["bold"]))
    try:
        response_direct = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {"role": "system", "content": "You are a helpful assistant. Provide only the final answer without any explanation."},
                {"role": "user", "content": text_prompt}
            ],
            temperature=0  # Use low temperature for deterministic answers
        )
        print(colored("Bot: ", "green") + response_direct.choices[0].message.content)
    except Exception as e:
         print(colored(f"Error: {e}", "red"))

    # 2. Chain of Thought Prompting (Zero-shot CoT with structured output)
    print(colored("\n--- 2. Chain of Thought (Zero-Shot structured) ---", "blue", attrs=["bold"]))
    try:
        response_cot = client.chat.completions.create(
            model=MODEL_ID,
            messages=[
                {
                    "role": "system", 
                    "content": (
                        "You are a careful AI assistant. Let's think step by step to solve the problem. "
                        "1. First, reason through the problem inside <thinking> tags. "
                        "2. Then, provide the final answer inside <answer> tags."
                    )
                },
                {"role": "user", "content": text_prompt}
            ],
            temperature=0
        )
        print(colored("Bot:\n", "green") + response_cot.choices[0].message.content)
    except Exception as e:
         print(colored(f"Error: {e}", "red"))

if __name__ == "__main__":
    main()

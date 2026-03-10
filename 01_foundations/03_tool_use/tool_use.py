import json
from openai import OpenAI
from termcolor import colored

# 1. Initialize Client
# Ollama supports function calling (tool use) with models like Llama 3.
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)
MODEL_ID = "llama3.2"

# 2. Define Local Tools (Functions)
# This is the actual Python code that will run on your machine.
def get_weather(location: str):
    """Simple mock function to simulate a weather API."""
    print(colored(f"  [System] Executing get_weather for: {location}", "magenta"))
    # In a real app, you'd call a real API here
    mock_weather_data = {
        "london": "22°C, Sunny",
        "new york": "18°C, Cloudy",
        "tokyo": "25°C, Rainy"
    }
    return mock_weather_data.get(location.lower(), "20°C, Unknown")

# 3. Define Tool Schemas
# We must tell the LLM what tools exist and what their parameters are.
tools = [
    {
        "type": "function",
        "function": {
            "name": "get_weather",
            "description": "Get the current weather in a given location",
            "parameters": {
                "type": "object",
                "properties": {
                    "location": {
                        "type": "string",
                        "description": "The city and state, e.g. San Francisco, CA",
                    },
                },
                "required": ["location"],
            },
        },
    }
]

def main():
    print(colored("🤖 Agentic AI - Level 1: Simple Tool Use", "cyan", attrs=["bold"]))
    
    # 4. Initial User Request
    messages = [
        {"role": "user", "content": "What's the weather like in London?"}
    ]
    
    print(colored("\nUser: ", "green") + messages[0]["content"])
    print(colored("Processing...", "cyan"))

    # 5. First LLM Call (Requesting Tool Use)
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=messages,
        tools=tools,
        tool_choice="auto",  # The model decides whether to use a tool
    )

    response_message = response.choices[0].message
    tool_calls = response_message.tool_calls

    # 6. Check if the model wants to call a tool
    if tool_calls:
        # The model can request multiple tool calls in one go
        messages.append(response_message)  # Add assistant's tool call to history

        for tool_call in tool_calls:
            function_name = tool_call.function.name
            function_args = json.loads(tool_call.function.arguments)
            
            print(colored(f"\nModel requested tool: {function_name}", "yellow"))
            print(colored(f"Arguments: {function_args}", "yellow"))

            # Dispatch to the actual Python function
            if function_name == "get_weather":
                function_response = get_weather(
                    location=function_args.get("location")
                )

                # 7. Add the TOOL result to messages
                # Note: 'tool_call_id' links the result to the specific request
                messages.append(
                    {
                        "tool_call_id": tool_call.id,
                        "role": "tool",
                        "name": function_name,
                        "content": function_response,
                    }
                )

        # 8. Second LLM Call (Final Answer)
        # We send the updated history (including tool results) back to the LLM
        final_response = client.chat.completions.create(
            model=MODEL_ID,
            messages=messages,
        )
        
        print(colored("\nBot: ", "blue") + final_response.choices[0].message.content)
    else:
        print(colored("\nBot: ", "blue") + response_message.content)

if __name__ == "__main__":
    main()

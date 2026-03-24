import json
import re
import math
from openai import OpenAI
from termcolor import colored

# 1. Initialize Client
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)
MODEL_ID = "llama3.2"

# 2. Define Mock Tools
def get_weather(location: str):
    """Mock weather API."""
    print(colored(f"  [Action] API Call: get_weather('{location}')", "magenta"))
    mock_data = {"london": "16°C", "new york": "20°C", "tokyo": "22°C"}
    temp = mock_data.get(location.lower(), "15°C")
    return temp

def calculate(expression: str):
    """Safe math evaluator with math functions."""
    print(colored(f"  [Action] Local Exec: calculate('{expression}')", "magenta"))
    try:
        # Add basic math functions to the Eval scope
        safe_dict = {
            "sqrt": math.sqrt,
            "pow": math.pow,
            "abs": abs,
            "round": round
        }
        # Remove units like °C if passed into the calculator
        clean_expr = expression.replace("°C", "").replace("°F", "")
        result = eval(clean_expr, {"__builtins__": None}, safe_dict)
        return str(result)
    except Exception as e:
        return f"Error: {e}"

# 3. System Prompt explaining the ReAct pattern
SYSTEM_PROMPT = """
You are an expert autonomous agent. You solve problems by using a ReAct (Reason + Act) loop.

AVAILABLE TOOLS:
1. get_weather(location: str): Returns the temperature in a city.
2. calculate(expression: str): Evaluates a mathematical expression (supports sqrt, pow, etc.).

STRICT RULES:
1. First, write a 'Thought:' explaining your reasoning.
2. If you need a tool, write 'Action: [tool_name]([arguments])' and then STOP.
3. Once you have an 'Observation:', use it in your next 'Thought:'.
4. If you have the answer, write 'Final Answer: [your response]'.

Example 1:
User: What is 5 + 5?
Thought: I need to calculate 5 + 5.
Action: calculate(5 + 5)
(Wait for Observation)
Observation: 10
Final Answer: 10

Example 2:
User: What is the weather in London?
Thought: I need to check the weather in London.
Action: get_weather("London")
(Wait for Observation)
Observation: 16°C
Final Answer: The weather in London is 16°C.
"""

def parse_action(text):
    """Finds Action: tool_name(args) in the text."""
    # Look for Action: name(args). Allow both single and double quotes or none.
    match = re.search(r"Action:\s*(\w+)\((.*)\)", text)
    if match:
        tool_name = match.group(1).strip()
        tool_args = match.group(2).strip().strip("'\"")
        return tool_name, tool_args
    return None, None

def main():
    print(colored("🛠️ Agentic AI - Level 2: Workflows - ReAct Pattern", "cyan", attrs=["bold"]))
    
    user_query = "What is the square root of the temperature in London right now?"
    print(colored(f"\nUser: {user_query}", "green"))

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_query}
    ]

    # ReAct Loop (limited to 5 turns to prevent infinite loops)
    for i in range(5):
        print(colored(f"\n--- Turn {i+1} ---", "yellow"))
        
        response = client.chat.completions.create(
            model=MODEL_ID,
            messages=messages,
            temperature=0,
            stop=["Observation:"] # Force the model to stop before it hallucinates an observation
        )
        
        agent_output = response.choices[0].message.content.strip()
        print(agent_output)
        
        # Check for Final Answer
        if "Final Answer:" in agent_output:
            # Print the final answer clearly
            final_match = re.search(r"Final Answer:\s*(.*)", agent_output)
            if final_match:
                print(colored(f"\nBot: {final_match.group(1)}", "blue", attrs=["bold"]))
            else:
                print(colored(f"\nBot: {agent_output}", "blue", attrs=["bold"]))
            break
        
        # Parse and Execute Action
        tool_name, tool_args = parse_action(agent_output)
        
        if tool_name:
            if tool_name == "get_weather":
                observation = get_weather(tool_args)
            elif tool_name == "calculate":
                observation = calculate(tool_args)
            else:
                observation = f"Error: Unknown tool {tool_name}"
            
            print(colored(f"Observation: {observation}", "blue"))
            
            # Feed the observation back to the model
            messages.append({"role": "assistant", "content": agent_output})
            messages.append({"role": "user", "content": f"Observation: {observation}"})
        else:
            if "Thought:" in agent_output:
                # If only a thought, encourage the model to provide an Action or Final Answer
                messages.append({"role": "assistant", "content": agent_output})
                messages.append({"role": "user", "content": "Please provide either an 'Action:' or a 'Final Answer:'."})
                continue
            
            print(colored("Error: Could not parse action from agent output.", "red"))
            break

if __name__ == "__main__":
    main()

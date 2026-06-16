import json
import sys
from typing import Literal
from pydantic import BaseModel, Field
from openai import OpenAI
from termcolor import colored

# Configure UTF-8 encoding for stdout/stderr to prevent UnicodeEncodeError on Windows
if hasattr(sys.stdout, 'reconfigure'):
    sys.stdout.reconfigure(encoding='utf-8')
if hasattr(sys.stderr, 'reconfigure'):
    sys.stderr.reconfigure(encoding='utf-8')

# 1. Initialize Client
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)
MODEL_ID = "llama3.2:3b"

# 2. Define the Router Schema
class RoutingDecision(BaseModel):
    route: Literal["TECHNICAL", "BILLING", "GENERAL"] = Field(
        description="The destination route for the user query."
    )
    reason: str = Field(
        description="A concise reason explaining why this query belongs to the chosen category."
    )
    confidence: float = Field(
        description="A confidence score between 0.0 and 1.0 indicating how certain the classification is."
    )

# 3. Define Agent Prompts
TECHNICAL_AGENT_PROMPT = """
You are a Senior Technical Support Engineer. You specialize in software development, APIs, configurations, and debugging technical issues.
Your goal is to provide precise, step-by-step, and technically accurate guidance. When helpful, provide clean code snippets.

Guidelines:
- Keep explanations clear and logical.
- Use code blocks for code snippets.
- Do not handle billing, payment, or general pricing questions. If they ask, redirect them back to billing.
"""

BILLING_AGENT_PROMPT = """
You are a Customer Billing Specialist. You handle issues regarding payments, subscriptions, refunds, invoices, and pricing plans.
You are professional, empathetic, and detail-oriented.

Guidelines:
- Reference mock account policies when appropriate (e.g., standard refund window is 14 days).
- Never disclose real financial details.
- Provide a breakdown of charges if asked.
- Do not solve coding or configuration issues. If they ask, redirect them to technical support.
"""

GENERAL_AGENT_PROMPT = """
You are a Customer Experience Representative. You handle greetings, general information, company info, and feedback.
You are warm, polite, and helpful.

Guidelines:
- Keep responses friendly and concise.
- Direct users to specific agents (Technical or Billing) if their questions become too technical or payment-related.
"""

# 4. Routing Function
def get_routing_decision(query: str) -> RoutingDecision:
    """Classifies the user query using structured JSON output from Ollama."""
    system_instruction = (
        "You are an intelligent routing agent. Your job is to classify incoming user queries "
        "into one of three categories: TECHNICAL, BILLING, or GENERAL.\n\n"
        "Categories definition:\n"
        "- TECHNICAL: Code issues, API integration problems, system errors, configurations, setup.\n"
        "- BILLING: Payments, subscription plans, pricing, invoices, refunds, charges.\n"
        "- GENERAL: Greetings, feedback, general small talk, or queries that do not fit the others.\n\n"
        "You must return a single JSON object with the following fields:\n"
        "{\n"
        "  \"route\": \"TECHNICAL\" | \"BILLING\" | \"GENERAL\",\n"
        "  \"reason\": \"string (brief explanation of why this route was selected)\",\n"
        "  \"confidence\": float (between 0.0 and 1.0)\n"
        "}\n\n"
        "Do not include any other keys or markdown formatting outside the JSON object."
    )
    
    prompt = f"User Query: \"{query}\"\n\nClassify this query."
    
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": system_instruction},
            {"role": "user", "content": prompt}
        ],
        response_format={"type": "json_object"},
        temperature=0  # Deterministic routing
    )
    
    raw_json = response.choices[0].message.content
    return RoutingDecision.model_validate_json(raw_json)

# 5. Specialist Agent Runners
def run_technical_agent(query: str) -> str:
    """Invokes the Technical Agent to answer the query."""
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": TECHNICAL_AGENT_PROMPT},
            {"role": "user", "content": query}
        ],
        temperature=0.2
    )
    return response.choices[0].message.content

def run_billing_agent(query: str) -> str:
    """Invokes the Billing Agent to answer the query."""
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": BILLING_AGENT_PROMPT},
            {"role": "user", "content": query}
        ],
        temperature=0.1
    )
    return response.choices[0].message.content

def run_general_agent(query: str) -> str:
    """Invokes the General Agent to answer the query."""
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[
            {"role": "system", "content": GENERAL_AGENT_PROMPT},
            {"role": "user", "content": query}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content

# 6. Main Execution Pipeline
def main():
    print(colored("➡️🤖 Agentic AI - Level 3: Systems - Routing & Classification", "cyan", attrs=["bold"]))
    print("----------------------------------------------------------------------")
    
    # Test Queries
    test_queries = [
        "Hi there! Just wanted to say hello and see what you can do.",
        "I need help setting up my connection. I keep getting a 'ConnectionRefusedError: [Errno 111] Connection refused' in Python. Here is my connection string: conn = establish_socket('localhost', 8080)",
        "Why was I billed $29.99 yesterday? My monthly subscription is supposed to be $19.99. Can you initiate a refund for the difference?"
    ]
    
    for idx, query in enumerate(test_queries, 1):
        print(colored(f"\n[Test Case {idx}] User Query:", "yellow", attrs=["bold"]))
        print(f"\"{query}\"")
        
        # Step 1: Route the query
        print(colored("\n[1/2] Routing intent...", "dark_grey"))
        try:
            decision = get_routing_decision(query)
            print(colored(" ✔ Router Decision:", "green", attrs=["bold"]))
            print(f"   - Selected Route: {colored(decision.route, 'cyan', attrs=['bold'])}")
            print(f"   - Reason:         {decision.reason}")
            print(f"   - Confidence:     {decision.confidence:.2f}")
            
            # Step 2: Handoff to target agent
            print(colored(f"\n[2/2] Handing off to {decision.route} Agent...", "dark_grey"))
            if decision.route == "TECHNICAL":
                agent_reply = run_technical_agent(query)
                agent_color = "blue"
            elif decision.route == "BILLING":
                agent_reply = run_billing_agent(query)
                agent_color = "magenta"
            else:
                agent_reply = run_general_agent(query)
                agent_color = "green"
            
            print(colored(f"\n--- Response from {decision.route} Agent ---", agent_color, attrs=["bold"]))
            print(agent_reply)
            
        except Exception as e:
            print(colored(f" ❌ Error in pipeline: {e}", "red"))
            
        print(colored("\n" + "="*70, "dark_grey"))

if __name__ == "__main__":
    main()

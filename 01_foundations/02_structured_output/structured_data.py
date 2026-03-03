import json
from typing import List, Optional
from pydantic import BaseModel, Field
from openai import OpenAI
from termcolor import colored

# 1. Initialize Client
client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="ollama"
)
MODEL_ID = "llama3"

# 2. Define the Schema
# We use Pydantic to define exactly what we want the LLM to return.
class UserProfile(BaseModel):
    name: str = Field(description="The full name of the person")
    age: int = Field(description="The age of the person")
    skills: List[str] = Field(description="A list of professional skills")
    location: Optional[str] = Field(description="City and country if mentioned", default=None)

def main():
    print(colored("🤖 Agentic AI - Level 1: Structured Output", "cyan", attrs=["bold"]))
    
    # 3. Unstructured Input
    input_text = """
    My name is Sarah Jenkins, I'm 28 years old and currently living in London. 
    I've spent the last 5 years working as a software engineer, specializing in 
    Python, React, and AWS Cloud architecture.
    """
    
    print(colored("\nRaw Text:", "yellow"))
    print(input_text.strip())

    # 4. Prepare the Prompt
    # We provide the schema to the LLM so it knows the structure.
    # Note: We are being very explicit that we want the DATA, not the schema.
    prompt = f"""
    Extract the following user information from the text provided.
    
    TEXT TO ANALYZE:
    {input_text}
    
    Return the extracted data as a SINGLE JSON object matching this structure:
    {{
        "name": "string",
        "age": integer,
        "skills": ["string"],
        "location": "string or null"
    }}
    
    Return ONLY the JSON. Do not include any explanation or the schema definition itself.
    """

    print(colored("\nRequesting Structured Data...", "cyan"))

    # 5. Call LLM with JSON Mode
    # Setting response_format is CRITICAL here.
    response = client.chat.completions.create(
        model=MODEL_ID,
        messages=[{"role": "user", "content": prompt}],
        response_format={"type": "json_object"}
    )

    # 6. Parse and Validate
    raw_json = response.choices[0].message.content
    print(colored("\nRaw JSON Response:", "green"))
    print(raw_json)

    try:
        # Validate using Pydantic
        # This gives us a real Python object with type checking!
        user_data = UserProfile.model_validate_json(raw_json)
        
        print(colored("\n✅ Successfully Parsed into Pydantic Object:", "blue", attrs=["bold"]))
        print(f"Name: {user_data.name}")
        print(f"Age: {user_data.age}")
        print(f"Skills: {', '.join(user_data.skills)}")
        print(f"Location: {user_data.location}")

    except Exception as e:
        print(colored(f"\n❌ Validation Failed: {e}", "red"))

if __name__ == "__main__":
    main()

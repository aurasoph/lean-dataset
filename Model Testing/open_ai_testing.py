from openai import OpenAI;
import os

api_key = os.environ.get("OPENAI_API_KEY")

client = OpenAI()

response = client.responses.create(
    model="gpt-4o",
    instructions="You are a coding assistant that talks like a pirate.",
    input="How do I check if a Python object is an instance of a class?",
)

print(response.output_text)

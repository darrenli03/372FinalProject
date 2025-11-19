from openai import OpenAI
import os

client = OpenAI()
client.api_key = os.getenv("openai_api_key")

def query_gpt(input_text):
    response = client.responses.create(
        model="gpt-5.1",
        input=input_text
    )
    return response.output_text

def construct_prompt(context, user_query):
    system_instructions = "Please provide a detailed response."
    return system_instructions + "\nContext: " + context + "\nUser Query: " + user_query

print(query_gpt("Hello, GPT! How are you today?"))

import openai
import os
import time
from dotenv import load_dotenv

load_dotenv()

openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_type = 'azure'
openai.api_version = '2024-02-01'
deployment_name = 'gpt-4o-mini'

def call_openai_with_retries(messages, max_tokens=1500, retries=5, wait_time=60):
    attempt = 1  
    while attempt <= retries:
        try:
            response = openai.ChatCompletion.create(
                engine=deployment_name,
                messages=messages,
                max_tokens=max_tokens
            )
            return response
        except openai.error.RateLimitError:
            print(f"Rate limit exceeded. Retrying in {wait_time} seconds... (Attempt {attempt}/{retries})")
            if attempt == retries:
                raise Exception("Max retries exceeded. Try again later.")  
            attempt += 1  
            time.sleep(wait_time)

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
            print(f"🔄 Attempt {attempt}/{retries} - Sending request to Azure OpenAI...")
            
            response = openai.ChatCompletion.create(
                engine=deployment_name,
                messages=messages,
                max_tokens=max_tokens
            )

            print(f"✅ OpenAI response received (tokens used: {response['usage']['total_tokens']})")
            return response

        except openai.error.RateLimitError:
            print(f"🚨 Rate limit exceeded. Retrying in {wait_time} seconds... (Attempt {attempt}/{retries})")
            if attempt == retries:
                print("🚨 Max retries exceeded. Giving up.")
                raise Exception("Max retries exceeded. Try again later.")  
            attempt += 1  
            time.sleep(wait_time)

        except openai.error.OpenAIError as e:
            print(f"🚨 OpenAI API Error: {str(e)}")
            raise e  # Re-raise the error so the API response logs it properly.


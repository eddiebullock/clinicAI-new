from flask import Flask, request, jsonify
import openai
import os
import time
from dotenv import load_dotenv
from asd_structure import ASD_REPORT_STRUCTURE  # Import modular structure
import re
from fuzzywuzzy import fuzz

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Set Azure OpenAI credentials
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_type = 'azure'
openai.api_version = '2024-02-01'

deployment_name = 'gpt-4o-mini'

# ✅ Retry logic for handling rate limits
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

# ✅ Extract relevant sections using expanded keyword matching
def extract_relevant_section(transcript, section_title):
    """
    Extracts relevant sections of text from the transcript based on section title.
    Uses keyword matching and fuzzy similarity to improve extraction accuracy.
    """
    keywords = section_title.lower().split()  # Break section title into keywords
    extracted_sentences = []

    # Split transcript into sentences while preserving structure
    sentences = re.split(r"(?<!\w\.\w.)(?<![A-Z][a-z]\.)(?<=\.|\?)\s", transcript)

    for sentence in sentences:
        if any(keyword in sentence.lower() for keyword in keywords):
            extracted_sentences.append(sentence)
        else:
            # Check for fuzzy similarity in phrasing
            for keyword in keywords:
                if fuzz.partial_ratio(keyword, sentence.lower()) > 70:  # Allow 70% similarity match
                    extracted_sentences.append(sentence)
                    break  # Avoid unnecessary extractions

    # If relevant details are found, keep them in full paragraphs
    if extracted_sentences:
        return " ".join(extracted_sentences)
    
    return "The transcript does not contain direct references to this topic, but based on related content, the individual may exhibit associated behaviors."

# ✅ Generate structured ASD report
def generate_asd_report(transcript):
    sections = []
    
    for category, content in ASD_REPORT_STRUCTURE.items():
        for section in content:
            section_title = section["title"]
            section_description = section.get("description", "Extract relevant details.")
            word_limit = section.get("word_limit", 600)  # Increased for longer narrative sections

            relevant_text = extract_relevant_section(transcript, section_title)

            messages = [
                {"role": "system", "content": (
                    "You are a clinical psychologist specializing in autism assessments. "
                    "Your task is to extract relevant details from the provided transcript "
                    "to create a structured, narrative-style psychological assessment report."
                    "Use full sentences and paragraphs instead of bullet points. When possible, "
                    "include direct quotes from the transcript to provide authenticity. "
                    "Ensure that the section is detailed, informative, and consistent with "
                    "clinical reports."
                )},
                {"role": "user", "content": (
                    f"Write a detailed and structured section for '{section_title}' based on the transcript.\n\n"
                    f"**Guidance:**\n{section_description}\n\n"
                    f"**Transcript:**\n{relevant_text}\n\n"
                    f"**Formatting Notes:**\n"
                    f"- The section should read like a clinical assessment report with full sentences.\n"
                    f"- If applicable, include direct quotes from the transcript to provide authenticity.\n"
                    f"- Maintain a professional, formal tone while preserving the personal nature of the assessment.\n"
                    f"- If no relevant details are found, indicate this subtly (e.g., 'The transcript does not contain direct references to...').\n"
                )}
            ]

            response = call_openai_with_retries(messages, max_tokens=word_limit * 2)
            sections.append({
                "title": section_title,
                "content": response['choices'][0]['message']['content'].strip()
            })

    return sections

# ✅ API Endpoint
@app.route('/generate_asd_report', methods=['POST'])
def generate_text():
    """
    API endpoint to process ASD assessment transcripts and return a structured report.
    Now supports both text and JSON input.
    """
    if request.content_type == "text/plain":
        transcript = request.data.decode("utf-8").strip()
    elif request.content_type == "application/json":
        data = request.json
        transcript = data.get("transcript", "").strip()
    else:
        return jsonify({"error": "Unsupported Content-Type. Use 'text/plain' or 'application/json'"}), 400

    if not transcript:
        return jsonify({"error": "No transcript provided"}), 400

    try:
        report_sections = generate_asd_report(transcript)
        return jsonify({"report": report_sections})
    except openai.error.OpenAIError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

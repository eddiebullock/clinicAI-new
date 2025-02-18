from flask import Flask, request, jsonify
import openai
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Set Azure OpenAI credentials
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_type = 'azure'
openai.api_version = '2024-02-01'

deployment_name = 'gpt-4o-mini'  # Ensure this matches your Azure deployment
MAX_TOKENS_PER_CHUNK = 8000  # Keep each chunk within safe limits

# Report Structure
ASD_REPORT_STRUCTURE = {
    "Assessment": [
        {"title": "Background", "word_limit": 500},
        {"title": "Key Mental Health Topics", "word_limit": 200},
        {"title": "Challenging Behavior", "word_limit": 200},
        {"title": "Academic History/Scholarly Skills", "word_limit": 250},
        {"title": "Family History", "word_limit": 200},
        {"title": "Past Medical History", "word_limit": 200},
        {"title": "Developmental History", "word_limit": 250}
    ],
    "Communication": [
        "Gesture", "Social Imaginative Play", "Conversational Interchange", "Repetitive or Unusual Speech"
    ],
    "Reciprocal Social Interaction": [
        "Nonverbal Behaviors to Regulate Emotion",
        "Developing Peer Relationships",
        "Shared Enjoyment",
        "Socioemotional Reciprocity"
    ],
    "Repetitive and Restrictive Behaviors": [
        "Preoccupation", "Routines", "Repetitive Movements",
        "Sensory Sensitivities", "Development at and Before 36 Months"
    ]
}

def split_text_into_chunks(text, max_tokens=MAX_TOKENS_PER_CHUNK):
    """
    Splits a long transcript into smaller chunks based on token limits.
    """
    words = text.split()
    chunks = []
    
    while words:
        chunk = words[:max_tokens]  # Take the first max_tokens words
        words = words[max_tokens:]  # Remove those words from the list
        chunks.append(" ".join(chunk))
    
    return chunks

def summarize_chunk(chunk):
    """
    Summarizes a single chunk using GPT.
    """
    response = openai.ChatCompletion.create(
        engine=deployment_name,
        messages=[
            {"role": "system", "content": "You are an expert clinical psychologist. Summarize the following ASD assessment transcript chunk."},
            {"role": "user", "content": f"Summarize this section: {chunk}"}
        ],
        max_tokens=1500  
    )

    return response['choices'][0]['message']['content'].strip()

def generate_asd_report(transcript):
    """
    Processes long transcripts by summarizing chunks first, then generating a structured report.
    """
    chunks = split_text_into_chunks(transcript)
    summarized_chunks = [summarize_chunk(chunk) for chunk in chunks]
    combined_summary = " ".join(summarized_chunks)

    return {"summary": combined_summary}

@app.route('/generate_asd_report', methods=['POST'])
def generate_text():
    """
    API endpoint to process ASD assessment transcripts and return a structured report.
    Supports both plain text and JSON input.
    """
    if request.content_type == "text/plain":
        transcript = request.data.decode("utf-8").strip()  # Read raw text input
    
    elif request.content_type == "application/json":
        data = request.json
        transcript = data.get("transcript", "").strip()
    
    else:
        return jsonify({"error": "Unsupported Content-Type. Use 'text/plain' or 'application/json'"}), 400

    if not transcript:
        return jsonify({"error": "No transcript provided"}), 400

    try:
        report = generate_asd_report(transcript)
        return jsonify(report)

    except openai.error.OpenAIError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
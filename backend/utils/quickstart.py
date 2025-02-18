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

# Predefined report structure for ASD assessments
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

def generate_asd_report(transcript):
    """
    Generates a structured ASD assessment report from a transcript.
    """
    sections = []
    
    for category, content in ASD_REPORT_STRUCTURE.items():
        if isinstance(content, list) and isinstance(content[0], dict):  # Sections with word limits
            for section in content:
                response = openai.ChatCompletion.create(
                    engine=deployment_name,
                    messages=[
                        {"role": "system", "content": f"You are an expert clinical psychologist. Convert ASD assessment transcripts into formal reports with structured sections."},
                        {"role": "user", "content": f"Extract and summarize the following section from the transcript:\n\n**Section:** {section['title']}\n**Word Limit:** {section['word_limit']} words\n\nTranscript:\n{transcript}"}
                    ],
                    max_tokens=section["word_limit"] * 2
                )

                sections.append({
                    "title": section["title"],
                    "content": response['choices'][0]['message']['content'].strip()
                })

        else:  # Section without word limits (bullet points)
            response = openai.ChatCompletion.create(
                engine=deployment_name,
                messages=[
                    {"role": "system", "content": "You are an expert clinical psychologist. Convert ASD assessment transcripts into structured bullet points for specific categories."},
                    {"role": "user", "content": f"Extract key details for **{category}** from the transcript under the following points:\n- " + "\n- ".join(content) + f"\n\nTranscript:\n{transcript}"}
                ],
                max_tokens=7000
            )

            sections.append({
                "title": category,
                "content": response['choices'][0]['message']['content'].strip()
            })

    return sections

@app.route('/generate_asd_report', methods=['POST'])
def generate_text():
    """
    API endpoint to process ASD assessment transcripts and return a structured report.
    Now supports both text and JSON input.
    """
    # Try to read raw text
    if request.content_type == "text/plain":
        transcript = request.data.decode("utf-8").strip()
    
    # Try to read JSON input
    elif request.content_type == "application/json":
        data = request.json
        transcript = data.get("transcript", "").strip()
    
    # Unsupported format
    else:
        return jsonify({"error": "Unsupported Content-Type. Use 'text/plain' or 'application/json'"}), 400

    # Check if transcript exists
    if not transcript:
        return jsonify({"error": "No transcript provided"}), 400

    try:
        report_sections = generate_asd_report(transcript)
        return jsonify({"report": report_sections})

    except openai.error.OpenAIError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

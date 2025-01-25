from flask import Blueprint, request, jsonify
import openai
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Initialize OpenAI API key
openai.api_key = os.getenv("OPENAI_API_KEY")

# Create a Blueprint for the report route
report_bp = Blueprint("report", __name__)

@report_bp.route("/generate_report", methods=["POST"])
def generate_report():
    try:
        # Retrieve the anonymized text from the request
        data = request.json
        anonymized_text = data.get("anonymized_text", "")

        if not anonymized_text.strip():
            return jsonify({"error": "No text provided"}), 400

        # Define the prompt for generating the report
        prompt = f"""
        You are an expert at creating assessment reports. Based on the anonymized text below, generate a structured assessment report. 
        Anonymized Text: {anonymized_text}

        Include the following sections:
        - Summary
        - Key Observations
        - Recommendations
        - Conclusion
        """

        # Call OpenAI's API using GPT-3.5
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # Use GPT-3.5 for cost efficiency
            messages=[{"role": "system", "content": prompt}],
            max_tokens=1000,
            temperature=0.7,
        )

        # Extract the generated text
        report_text = response['choices'][0]['message']['content']

        return jsonify({"message": "Report generated successfully", "report": report_text}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to generate report: {str(e)}"}), 500

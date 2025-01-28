from flask import Blueprint, request, jsonify
from sections.assessment import generate_assessment_report
from sections.communication import generate_communication_report
from sections.reciprocal_social_interaction import generate_rsi_report
from sections.rrb import generate_rrb_report
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

report_bp = Blueprint("report", __name__)

@report_bp.route("/generate_report", methods=["POST"])
def generate_report():
    try:
        # Retrieve clinician's notes from the request
        data = request.json
        anonymized_text = data.get("anonymized_text", "")

        if not anonymized_text.strip():
            return jsonify({"error": "No text provided"}), 400

        # Log the received input
        print(f"Anonymized text received: {anonymized_text}")

        # Generate reports for each section
        assessment = generate_assessment_report(anonymized_text)
        print(f"Assessment generated: {assessment}")  # Debug log

        communication = generate_communication_report(anonymized_text)
        print(f"Communication generated: {communication}")  # Debug log

        rsi = generate_rsi_report(anonymized_text)
        print(f"Reciprocal social interaction generated: {rsi}")  # Debug log

        rrb = generate_rrb_report(anonymized_text)
        print(f"Restricted and repetitive behaviors generated: {rrb}")  # Debug log

        # Combine all sections into a final report
        full_report = f"""
        Autism Assessment Report

        Section 1: Background and Key Topics
        {assessment}

        Section 2: Communication
        {communication}

        Section 3: Reciprocal Social Interaction
        {rsi}

        Section 4: Restricted and Repetitive Behaviors
        {rrb}
        """

        print("Full report generated successfully.")  # Debug log
        return jsonify({"message": "Report generated successfully", "report": full_report}), 200

    except Exception as e:
        print("Error generating report:", str(e))
        return jsonify({"error": f"Failed to generate report: {str(e)}"}), 500

from flask import Blueprint, request, jsonify
from sections.assessment import generate_assessment_report
from sections.communication import generate_communication_report
from sections.reciprocal_social_interaction import generate_rsi_report
from sections.rrb import generate_rrb_report
from utils.model import call_local_model

import requests

report_bp = Blueprint("report", __name__)

def generate_section_with_timeout(func, text, section_name, timeout=120):
    """
    Calls the function with a timeout and handles errors gracefully.
    """
    try:
        response = func(text)
        return response if response else f"⚠️ {section_name} report generation returned empty."
    except requests.exceptions.Timeout:
        return f"⚠️ {section_name} report generation timed out after {timeout} seconds."
    except Exception as e:
        return f"⚠️ Error generating {section_name} report: {str(e)}"

@report_bp.route("/generate_report", methods=["POST"])
def generate_report():
    try:
        # Retrieve clinician's notes from the request
        data = request.json
        anonymized_text = data.get("anonymized_text", "")

        if not anonymized_text.strip():
            return jsonify({"error": "No text provided"}), 400

        print(f"Anonymized text received: {anonymized_text}")

        # Sequentially generate each section to prevent CPU overload
        assessment = generate_section_with_timeout(generate_assessment_report, anonymized_text, "Assessment")
        communication = generate_section_with_timeout(generate_communication_report, anonymized_text, "Communication")
        rsi = generate_section_with_timeout(generate_rsi_report, anonymized_text, "Reciprocal Social Interaction")
        rrb = generate_section_with_timeout(generate_rrb_report, anonymized_text, "Restricted and Repetitive Behaviors")

        # Combine sections into a formatted report
        full_report = f"""
        <h1 style="text-align:center;">Autism Assessment Report</h1>

        <h2>Background and Key Topics</h2>
        {format_subsections(assessment)}

        <h2>Communication</h2>
        {format_subsections(communication)}

        <h2>Reciprocal Social Interaction</h2>
        {format_subsections(rsi)}

        <h2>Restricted and Repetitive Behaviors</h2>
        {format_subsections(rrb)}
        """

        print("Full report generated successfully.")  
        return jsonify({"message": "Report generated successfully", "report": full_report}), 200

    except Exception as e:
        print("Error generating report:", str(e))
        return jsonify({"error": f"Failed to generate report: {str(e)}"}), 500

def format_subsections(section_text):
    """
    Formats subheadings and paragraphs properly.
    """
    import re

    formatted_text = section_text
    formatted_text = re.sub(r"\*\*(.*?)\*\*", r"<h3>\1</h3>\n", formatted_text)
    formatted_text = re.sub(r"(\d+\.)", r"\n\1 ", formatted_text)
    
    paragraphs = formatted_text.split("\n")
    formatted_text = "".join(
        f"<p>{para.strip()}</p>\n" if not para.strip().startswith("<h3>") else para for para in paragraphs
    )

    return formatted_text

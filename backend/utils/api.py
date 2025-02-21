from flask import Flask, request, jsonify
from asd_processing import generate_asd_report
from adhd_processing import generate_adhd_report
import os
from flask_cors import CORS

app = Flask(__name__)
CORS(app)  # Allow all origins (for development)

@app.route('/generate_report', methods=['POST'])
def generate_text():
    """Handles the report generation for ADHD and ASD based on the uploaded transcript file."""
    
    if 'file' not in request.files:
        print("🚨 ERROR: No file uploaded")
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    assessment_type = request.form.get('assessment_type', '').strip().lower()

    if not file or not assessment_type:
        print("🚨 ERROR: Missing file or assessment type")
        return jsonify({"error": "Missing file or assessment type"}), 400

    if assessment_type not in ["asd", "adhd"]:
        print(f"🚨 ERROR: Invalid assessment type '{assessment_type}'")
        return jsonify({"error": "Invalid assessment type. Choose 'asd' or 'adhd'"}), 400

    # Read transcript from the uploaded file
    transcript = file.read().decode('utf-8')
    print(f"✅ Transcript successfully read ({len(transcript)} characters)")
    print(f"✅ Assessment Type: {assessment_type}")

    try:
        if assessment_type == "asd":
            print("🛠️ Generating ASD Report...")
            report_sections = generate_asd_report(transcript)
        else:
            print("🛠️ Generating ADHD Report...")
            report_sections = generate_adhd_report(transcript)

        print(f"✅ Report successfully generated with {len(report_sections)} sections.")
        return jsonify({"report": report_sections})

    except Exception as e:
        print(f"🚨 ERROR DURING REPORT GENERATION: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

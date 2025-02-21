from flask import Flask, request, jsonify
from asd_processing import generate_asd_report
from adhd_processing import generate_adhd_report

app = Flask(__name__)

@app.route('/generate_report', methods=['POST'])
def generate_text():
    data = request.json
    transcript = data.get("transcript", "").strip()
    assessment_type = data.get("assessment_type", "").strip().lower()

    if not transcript:
        return jsonify({"error": "No transcript provided"}), 400
    if assessment_type not in ["asd", "adhd"]:
        return jsonify({"error": "Invalid assessment type. Choose 'asd' or 'adhd'"}), 400

    try:
        if assessment_type == "asd":
            report_sections = generate_asd_report(transcript)
        else:
            report_sections = generate_adhd_report(transcript)

        return jsonify({"report": report_sections})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

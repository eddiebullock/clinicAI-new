from flask import Blueprint, request, jsonify
from services.anonymizer import anonymize_text_with_huggingface

# Blueprint for the upload route
upload_bp = Blueprint("upload", __name__)

@upload_bp.route("/anonymize", methods=["POST"])
def anonymize_text():
    # Get text input from the user
    data = request.json
    text = data.get("text", "")

    if not text.strip():
        return jsonify({"error": "No text provided"}), 400

    try:
        # Chunk the text for anonymization
        anonymized_text = ""
        chunk_size = 1000  # Split text into chunks of 1000 characters
        for i in range(0, len(text), chunk_size):
            chunk = text[i:i + chunk_size]
            anonymized_chunk = anonymize_text_with_huggingface(chunk)
            anonymized_text += anonymized_chunk + "\n"

        # Return anonymized text
        return jsonify({"message": "Text anonymized successfully", "anonymized_text": anonymized_text}), 200
    except Exception as e:
        return jsonify({"error": f"Failed to anonymize text: {str(e)}"}), 500

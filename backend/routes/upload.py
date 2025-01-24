import os
from flask import Blueprint, request, jsonify
from services.anonymizer import anonymize_text_with_huggingface

# Blueprint for the upload route
upload_bp = Blueprint("upload", __name__)

# Set a temporary upload directory
UPLOAD_FOLDER = "./uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Allowed file extensions
ALLOWED_EXTENSIONS = {"txt"}

# Function to validate file type
def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@upload_bp.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "No file part in the request"}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No file selected"}), 400

    if not allowed_file(file.filename):
        return jsonify({"error": "File type not allowed"}), 400

    # Save the file temporarily
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Anonymize the file content using Hugging Face
    try:
        anonymized_content = anonymize_text_with_huggingface(file_path)
        anonymized_file_path = os.path.join(UPLOAD_FOLDER, f"anonymized_{file.filename}")
        with open(anonymized_file_path, "w") as anon_file:
            anon_file.write(anonymized_content)
    except Exception as e:
        return jsonify({"error": f"Failed to anonymize file: {str(e)}"}), 500

    return jsonify({
        "message": "File uploaded and anonymized successfully",
        "original_file_path": file_path,
        "anonymized_file_path": anonymized_file_path
    }), 200

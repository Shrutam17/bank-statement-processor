import os
import uuid
from datetime import datetime
from pathlib import Path

from flask import Flask, jsonify, render_template, request, send_file
from werkzeug.utils import secure_filename

from src.pipeline import BankStatementPipeline
from src.security.file_validator import FileValidationError
from src.utils.logger import get_logger

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 50 * 1024 * 1024  # 50MB max file size
app.config["UPLOAD_FOLDER"] = "uploads"
app.config["OUTPUT_FOLDER"] = "outputs"

logger = get_logger(__name__)

# Ensure folders exist
Path(app.config["UPLOAD_FOLDER"]).mkdir(exist_ok=True)
Path(app.config["OUTPUT_FOLDER"]).mkdir(exist_ok=True)

pipeline = BankStatementPipeline()


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/api/upload", methods=["POST"])
def upload_pdf():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file provided"}), 400

        file = request.files["file"]
        if file.filename == "":
            return jsonify({"error": "No file selected"}), 400

        if not file.filename.lower().endswith(".pdf"):
            return jsonify({"error": "Only PDF files are allowed"}), 400

        # Generate unique filename
        original_filename = secure_filename(file.filename)
        unique_id = str(uuid.uuid4())[:8]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{unique_id}_{original_filename}"
        filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)

        # Save uploaded file
        file.save(filepath)
        logger.info(f"File uploaded: {filename}")

        # Get export formats from request
        formats = request.form.getlist("formats[]")
        if not formats:
            formats = ["xlsx", "csv"]

        # Process the PDF
        result = pipeline.process(filepath, export_formats=formats)

        # Prepare response
        response = {
            "success": True,
            "job_id": unique_id,
            "filename": original_filename,
            "pdf_type": result["pdf_type"],
            "transaction_count": result["transaction_count"],
            "account_details": result["account_details"],
            "output_files": {},
        }

        # Add download links for output files
        for fmt, path in result["output_paths"].items():
            output_filename = os.path.basename(path)
            response["output_files"][fmt] = {
                "filename": output_filename,
                "download_url": f"/api/download/{output_filename}",
            }

        # Clean up uploaded file
        try:
            os.remove(filepath)
        except Exception as e:
            logger.warning(f"Failed to remove uploaded file: {e}")

        return jsonify(response), 200

    except FileValidationError as e:
        logger.error(f"Validation error: {e}")
        return jsonify({"error": f"Validation error: {str(e)}"}), 400

    except Exception as e:
        logger.error(f"Processing error: {e}", exc_info=True)
        return jsonify({"error": f"Processing failed: {str(e)}"}), 500


@app.route("/api/download/<filename>")
def download_file(filename):
    try:
        # Security: only allow alphanumeric, dots, underscores, and hyphens
        safe_filename = secure_filename(filename)
        filepath = os.path.join(app.config["OUTPUT_FOLDER"], safe_filename)

        if not os.path.exists(filepath):
            return jsonify({"error": "File not found"}), 404

        return send_file(
            filepath,
            as_attachment=True,
            download_name=safe_filename,
        )

    except Exception as e:
        logger.error(f"Download error: {e}")
        return jsonify({"error": "Download failed"}), 500


@app.route("/api/health")
def health():
    return jsonify({"status": "healthy", "service": "Bank Statement Processor"}), 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)

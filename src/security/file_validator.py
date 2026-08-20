import os

from src.utils.config_loader import load_config

PDF_MAGIC_BYTES = b"%PDF-"


class FileValidationError(Exception):
    pass


def validate_pdf_file(file_path):
    config = load_config()
    max_size_bytes = config["app"]["max_file_size_mb"] * 1024 * 1024

    if not os.path.isfile(file_path):
        raise FileValidationError(f"File not found: {file_path}")

    if not file_path.lower().endswith(".pdf"):
        raise FileValidationError("Only .pdf files are supported")

    file_size = os.path.getsize(file_path)
    if file_size == 0:
        raise FileValidationError("File is empty")
    if file_size > max_size_bytes:
        raise FileValidationError(
            f"File size {file_size} bytes exceeds limit of {max_size_bytes} bytes"
        )

    with open(file_path, "rb") as f:
        header = f.read(5)
    if header != PDF_MAGIC_BYTES:
        raise FileValidationError("File does not have a valid PDF header, possible spoofed file")

    return True


def validate_page_count(page_count):
    config = load_config()
    max_pages = config["security"]["max_pages"]
    if page_count > max_pages:
        raise FileValidationError(
            f"Document has {page_count} pages, exceeds max allowed {max_pages}"
        )
    return True


def sanitize_filename(filename):
    keep_chars = (" ", ".", "_", "-")
    cleaned = "".join(c for c in filename if c.isalnum() or c in keep_chars).strip()
    return cleaned.replace(" ", "_") or "unnamed_file.pdf"

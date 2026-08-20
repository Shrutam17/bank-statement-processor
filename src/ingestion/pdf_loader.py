import fitz

from src.security.file_validator import validate_pdf_file, validate_page_count
from src.utils.logger import get_logger

logger = get_logger(__name__)


class PDFLoadError(Exception):
    pass


def load_pdf(file_path):
    validate_pdf_file(file_path)
    try:
        doc = fitz.open(file_path)
    except Exception as exc:
        raise PDFLoadError(f"Unable to open PDF: {exc}") from exc

    if doc.needs_pass:
        doc.close()
        raise PDFLoadError("PDF is password protected, encrypted PDFs are not supported")

    validate_page_count(doc.page_count)
    logger.info(f"Loaded PDF {file_path} with {doc.page_count} pages")
    return doc

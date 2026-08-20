import pdfplumber

from src.utils.logger import get_logger

logger = get_logger(__name__)


def extract_text_pages(file_path):
    pages_text = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            pages_text.append(page.extract_text() or "")
    logger.info(f"Extracted text from {len(pages_text)} pages using pdfplumber")
    return pages_text


def extract_tables(file_path):
    all_tables = []
    with pdfplumber.open(file_path) as pdf:
        for page in pdf.pages:
            tables = page.extract_tables()
            for table in tables:
                if table and len(table) > 1:
                    all_tables.append(table)
    logger.info(f"Extracted {len(all_tables)} candidate tables")
    return all_tables

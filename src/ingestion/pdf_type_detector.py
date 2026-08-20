from src.utils.logger import get_logger

logger = get_logger(__name__)

MIN_CHARS_PER_PAGE_FOR_TEXT = 40


def detect_pdf_type(doc):
    total_chars = 0
    pages_checked = min(doc.page_count, 3)

    for page_index in range(pages_checked):
        page = doc.load_page(page_index)
        text = page.get_text("text")
        total_chars += len(text.strip())

    avg_chars_per_page = total_chars / pages_checked if pages_checked else 0
    pdf_type = "text" if avg_chars_per_page >= MIN_CHARS_PER_PAGE_FOR_TEXT else "image"

    logger.info(f"Detected PDF type: {pdf_type} (avg {avg_chars_per_page:.1f} chars/page)")
    return pdf_type

import pytesseract
from pdf2image import convert_from_path

from src.utils.config_loader import load_config
from src.utils.logger import get_logger

logger = get_logger(__name__)


def extract_text_pages_ocr(file_path):
    """
    Extract text from image-based/scanned PDFs using OCR.
    
    Note: OCR accuracy depends heavily on scan quality. For best results:
    - Use scans at 300 DPI or higher
    - Ensure good contrast and no skew
    - Clean, legible fonts
    """
    config = load_config()
    dpi = config["app"]["ocr_dpi"]

    images = convert_from_path(file_path, dpi=dpi)
    pages_text = []
    for index, image in enumerate(images):
        preprocessed = _preprocess_image(image)
        text = pytesseract.image_to_string(preprocessed)
        pages_text.append(text)
        logger.info(f"OCR completed for page {index + 1}/{len(images)}")

    return pages_text


def _preprocess_image(image):
    """Simple grayscale preprocessing for OCR"""
    grayscale = image.convert("L")
    return grayscale

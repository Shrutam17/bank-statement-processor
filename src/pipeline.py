import os

from src.classification.classifier_engine import ClassifierEngine
from src.export.csv_exporter import export_to_csv
from src.export.excel_exporter import export_to_excel
from src.extraction.account_extractor import extract_account_details
from src.extraction.ocr_extractor import extract_text_pages_ocr
from src.extraction.text_extractor import extract_tables, extract_text_pages
from src.extraction.transaction_parser import (
    parse_transactions_from_tables,
    parse_transactions_from_text,
)
from src.ingestion.pdf_loader import load_pdf
from src.ingestion.pdf_type_detector import detect_pdf_type
from src.security.file_validator import sanitize_filename
from src.utils.config_loader import load_config, resolve_path
from src.utils.logger import get_logger

logger = get_logger(__name__)


class BankStatementPipeline:
    def __init__(self):
        self.config = load_config()
        self.classifier_engine = ClassifierEngine()
        
        # Extraction method configuration
        self.extraction_method = self.config.get("extraction", {}).get("method", "traditional")
        logger.info(f"Pipeline initialized with extraction method: {self.extraction_method}")

    def process(self, file_path, export_formats=("xlsx", "csv")):
        logger.info(f"Starting pipeline for {file_path}")

        # Choose extraction method
        if self.extraction_method == "llm":
            result = self._process_with_llm(file_path)
        elif self.extraction_method == "hybrid":
            result = self._process_hybrid(file_path)
        else:
            result = self._process_traditional(file_path)
        
        # Classify transactions (always non-LLM as per assessment)
        result["transactions"] = self.classifier_engine.classify_batch(result["transactions"])

        # Export results
        output_paths = self._export(
            file_path, 
            result["transactions"], 
            result["account_details"], 
            export_formats
        )

        logger.info(
            f"Pipeline completed for {file_path}, "
            f"{len(result['transactions'])} transactions processed"
        )
        
        return {
            "pdf_type": result.get("pdf_type", "unknown"),
            "extraction_method": result.get("extraction_method", self.extraction_method),
            "account_details": result["account_details"],
            "transaction_count": len(result["transactions"]),
            "transactions": result["transactions"],
            "output_paths": output_paths,
        }
    
    def _process_with_llm(self, file_path):
        """Process using LLM extraction"""
        try:
            from src.extraction.llm_extractor import LLMExtractor
            
            logger.info("Using LLM extraction")
            llm_extractor = LLMExtractor()
            result = llm_extractor.extract(file_path)
            
            return {
                "pdf_type": "llm-processed",
                "extraction_method": "llm",
                "account_details": result["account_details"],
                "transactions": result["transactions"],
            }
        except Exception as e:
            logger.error(f"LLM extraction failed: {e}")
            
            # Check if fallback is enabled
            if self.config.get("extraction", {}).get("llm", {}).get("fallback_to_traditional", False):
                logger.warning("Falling back to traditional extraction")
                return self._process_traditional(file_path)
            else:
                raise
    
    def _process_hybrid(self, file_path):
        """Try traditional first, use LLM if confidence is low"""
        logger.info("Using hybrid extraction (traditional with LLM fallback)")
        
        # Try traditional first
        result = self._process_traditional(file_path)
        
        # Check if we should use LLM
        transaction_count = len(result["transactions"])
        
        # Use LLM if: no transactions found OR account name not extracted
        should_use_llm = (
            transaction_count == 0 or
            not result["account_details"].get("account_holder_name")
        )
        
        if should_use_llm:
            logger.info(
                f"Traditional extraction had issues "
                f"(transactions: {transaction_count}), trying LLM"
            )
            try:
                return self._process_with_llm(file_path)
            except Exception as e:
                logger.warning(f"LLM fallback failed: {e}, using traditional result")
        
        result["extraction_method"] = "traditional"
        return result
    
    def _process_traditional(self, file_path):
        """Traditional extraction (existing logic)"""
        doc = load_pdf(file_path)
        pdf_type = detect_pdf_type(doc)
        doc.close()

        if pdf_type == "text":
            pages_text = extract_text_pages(file_path)
            tables = extract_tables(file_path)
        else:
            pages_text = extract_text_pages_ocr(file_path)
            tables = []

        full_text = "\n".join(pages_text)
        account_details = extract_account_details(full_text)

        transactions = parse_transactions_from_tables(tables)
        if not transactions:
            transactions = parse_transactions_from_text(pages_text)
        
        return {
            "pdf_type": pdf_type,
            "extraction_method": "traditional",
            "account_details": account_details,
            "transactions": transactions,
        }

    def _export(self, file_path, transactions, account_details, export_formats):
        output_dir = resolve_path(self.config["paths"]["outputs"])
        os.makedirs(output_dir, exist_ok=True)

        base_name = sanitize_filename(os.path.splitext(os.path.basename(file_path))[0])
        output_paths = {}

        if "xlsx" in export_formats:
            excel_path = os.path.join(output_dir, f"{base_name}.xlsx")
            output_paths["xlsx"] = export_to_excel(transactions, excel_path, account_details)

        if "csv" in export_formats:
            csv_path = os.path.join(output_dir, f"{base_name}.csv")
            output_paths["csv"] = export_to_csv(transactions, csv_path)

        return output_paths

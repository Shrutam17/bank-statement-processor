import csv

from src.utils.logger import get_logger

logger = get_logger(__name__)

COLUMNS = ["date", "description", "debit", "credit", "balance", "category", "classification_confidence"]


def export_to_csv(transactions, output_path):
    with open(output_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        writer.writeheader()
        for txn in transactions:
            writer.writerow(txn)

    logger.info(f"Exported {len(transactions)} transactions to CSV at {output_path}")
    return output_path

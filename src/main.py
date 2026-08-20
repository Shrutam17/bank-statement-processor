import argparse
import json
import sys

from src.pipeline import BankStatementPipeline


def main():
    parser = argparse.ArgumentParser(description="Bank statement processing and classification system")
    parser.add_argument("pdf_path", help="Path to the bank statement PDF")
    parser.add_argument(
        "--formats",
        nargs="+",
        default=["xlsx", "csv"],
        choices=["xlsx", "csv"],
        help="Export formats to generate",
    )
    parser.add_argument("--summary-json", action="store_true", help="Print run summary as JSON")
    args = parser.parse_args()

    pipeline = BankStatementPipeline()
    result = pipeline.process(args.pdf_path, export_formats=args.formats)

    if args.summary_json:
        summary = {
            "pdf_type": result["pdf_type"],
            "transaction_count": result["transaction_count"],
            "output_paths": result["output_paths"],
        }
        print(json.dumps(summary, indent=2))
    else:
        print(f"PDF type detected: {result['pdf_type']}")
        print(f"Transactions extracted: {result['transaction_count']}")
        print(f"Account holder: {result['account_details'].get('account_holder_name')}")
        for fmt, path in result["output_paths"].items():
            print(f"Exported {fmt}: {path}")

    return 0


if __name__ == "__main__":
    sys.exit(main())

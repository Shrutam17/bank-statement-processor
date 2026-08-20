import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from src.extraction.transaction_parser import parse_transactions_from_text, _parse_amount


def test_parse_amount_handles_commas():
    assert _parse_amount("12,345.50") == 12345.50


def test_parse_amount_handles_empty():
    assert _parse_amount("") == 0.0


def test_parse_transactions_from_text_extracts_date_and_amounts():
    page_text = "01/03/2026 SALARY CREDIT INFOSYS LTD 25000.00 75000.00"
    transactions = parse_transactions_from_text([page_text])
    assert len(transactions) == 1
    assert transactions[0]["date"] == "01/03/2026"
    assert transactions[0]["balance"] == 75000.00

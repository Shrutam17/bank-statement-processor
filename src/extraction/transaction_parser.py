import re

from src.utils.logger import get_logger

logger = get_logger(__name__)

# Updated date pattern to handle both real dates and common date placeholders
DATE_PATTERN = re.compile(r"\b(\d{1,2}[-/]\d{1,2}[-/]\d{2,4})\b")
# Pattern for date placeholders like mm/dd/yyyy, dd/mm/yyyy
DATE_PLACEHOLDER_PATTERN = re.compile(r"\b(mm/dd/yyyy|dd/mm/yyyy|yyyy-mm-dd|mm-dd-yyyy)\b", re.IGNORECASE)
AMOUNT_PATTERN = re.compile(r"-?(?:\d{1,3}(?:,\d{2,3})+|\d+)(?:\.\d{1,2})?")

HEADER_ALIASES = {
    "date": [
        "date", "txn date", "value date", "transaction date", "trans date",
        "posting date", "transaction dt", "dt", "tran date", "effective date",
        "txn dt", "date of transaction", "trans dt"
    ],
    "description": [
        "description", "narration", "particulars", "details", "remarks",
        "transaction", "reference", "memo", "notes", "transaction details",
        "desc", "transaction description", "ref", "payment details"
    ],
    "debit": [
        "debit", "withdrawal", "dr", "debit amount", "withdrawal amt",
        "withdrawals", "debits", "payment", "paid out", "expense",
        "debit amt", "dr amount", "debit rs", "paid", "debit inr"
    ],
    "credit": [
        "credit", "deposit", "cr", "credit amount", "deposit amt",
        "deposits", "credits", "received", "income",
        "credit amt", "cr amount", "credit rs", "received amt", "credit inr"
    ],
    "balance": [
        "balance", "closing balance", "available balance", "bal",
        "running balance", "account balance", "balance amt",
        "available bal", "current balance", "bal amt", "closing bal"
    ],
}


def parse_transactions_from_tables(tables):
    transactions = []
    for table in tables:
        if not table or len(table) < 2:
            continue
            
        header_row = table[0]
        column_map = _map_columns(header_row)
        
        # Must have at least date column to be valid transaction table
        if "date" not in column_map:
            continue

        for row in table[1:]:
            # Skip empty rows or end markers
            if not row or all(not cell for cell in row):
                continue
            
            # Check for end markers
            first_cell = str(row[0] if row else "").lower()
            if "end of transaction" in first_cell or "---" in first_cell:
                break
                
            record = _build_record_from_row(row, column_map)
            if record:
                transactions.append(record)

    logger.info(f"Parsed {len(transactions)} transactions from tables")
    return transactions


def _map_columns(header_row):
    column_map = {}
    for index, cell in enumerate(header_row):
        if not cell:
            continue
        cell_normalized = cell.strip().lower()
        for field, aliases in HEADER_ALIASES.items():
            if any(alias in cell_normalized for alias in aliases):
                column_map[field] = index
                break
    return column_map


def _build_record_from_row(row, column_map):
    def get_cell(field):
        index = column_map.get(field)
        if index is None or index >= len(row) or row[index] is None:
            return ""
        return str(row[index]).strip()

    date_value = get_cell("date")
    
    # Skip if date is empty or is a placeholder like "mm/dd/yyyy"
    if not date_value:
        return None
    if DATE_PLACEHOLDER_PATTERN.match(date_value):
        logger.debug(f"Skipping row with placeholder date: {date_value}")
        return None
    
    # Check if it contains an actual date pattern
    if not DATE_PATTERN.search(date_value):
        return None

    debit = _parse_amount(get_cell("debit"))
    credit = _parse_amount(get_cell("credit"))
    balance = _parse_amount(get_cell("balance"))
    
    description = get_cell("description") or "N/A"
    
    # Skip if description looks like a header or separator
    desc_lower = description.lower()
    if any(skip in desc_lower for skip in ["end of transaction", "---", "total", "subtotal"]):
        return None

    return {
        "date": date_value,
        "description": description,
        "debit": debit,
        "credit": credit,
        "balance": balance,
    }


def parse_transactions_from_text(pages_text):
    transactions = []
    for page_text in pages_text:
        for line in page_text.splitlines():
            record = _parse_line(line)
            if record:
                transactions.append(record)

    logger.info(f"Parsed {len(transactions)} transactions from raw text fallback")
    return transactions


def _parse_line(line):
    line = line.strip()
    date_match = DATE_PATTERN.search(line)
    if not date_match:
        return None

    # Extract all amounts from the line after the date
    after_date = line[date_match.end():]
    amounts = AMOUNT_PATTERN.findall(after_date)
    amounts = [a for a in amounts if a not in ("", "-")]
    
    # Need at least 2 amounts (transaction amount and balance)
    if len(amounts) < 2:
        return None

    # Get description (text between date and first amount)
    first_amount_pos = after_date.find(amounts[0])
    description = after_date[:first_amount_pos].strip(" -:|") if first_amount_pos > 0 else "N/A"
    if not description or description == "":
        description = "N/A"

    # Parse amounts
    parsed_amounts = [_parse_amount(a) for a in amounts]
    
    # Determine debit/credit based on number of amounts and patterns
    if len(parsed_amounts) == 2:
        # Two amounts: could be [debit, balance] or [credit, balance]
        txn_amount = parsed_amounts[0]
        balance = parsed_amounts[1]
        is_debit = _guess_is_debit(description)
        debit = txn_amount if is_debit else 0.0
        credit = 0.0 if is_debit else txn_amount
    elif len(parsed_amounts) == 3:
        # Three amounts: likely [debit, credit, balance] or [amount, amount, balance]
        # Check if one of the first two is 0 or very small
        amount1, amount2, balance = parsed_amounts
        if amount1 > 0 and amount2 == 0:
            # Debit transaction
            debit = amount1
            credit = 0.0
        elif amount1 == 0 and amount2 > 0:
            # Credit transaction
            debit = 0.0
            credit = amount2
        elif amount1 > 0 and amount2 > 0:
            # Both have values - use heuristic
            is_debit = _guess_is_debit(description)
            if is_debit:
                debit = amount1
                credit = 0.0
            else:
                debit = 0.0
                credit = amount2
        else:
            # Fallback to heuristic
            is_debit = _guess_is_debit(description)
            debit = amount1 if is_debit else 0.0
            credit = amount2 if not is_debit else 0.0
    else:
        # More than 3 amounts - take last as balance, second to last as transaction
        balance = parsed_amounts[-1]
        txn_amount = parsed_amounts[-2]
        is_debit = _guess_is_debit(description)
        debit = txn_amount if is_debit else 0.0
        credit = 0.0 if is_debit else txn_amount

    return {
        "date": date_match.group(1),
        "description": description,
        "debit": debit,
        "credit": credit,
        "balance": balance,
    }


def _guess_is_debit(description):
    """Determine if transaction is likely a debit based on keywords"""
    debit_hints = [
        "withdrawal", "purchase", "paid", "atm", "dr", "debit",
        "payment", "emi", "loan", "bill", "order", "transfer to",
        "fund transfer", "subscription", "uber", "swiggy", "amazon",
        "netflix", "bigbasket", "rent", "zerodha"
    ]
    credit_hints = [
        "salary", "credit", "deposit", "interest", "refund", "cr",
        "reversal", "cashback"
    ]
    
    description_lower = description.lower()
    
    # Check credit hints first (higher priority)
    if any(hint in description_lower for hint in credit_hints):
        return False
    
    # Check debit hints
    if any(hint in description_lower for hint in debit_hints):
        return True
    
    # Default to debit if unsure
    return True


def _parse_amount(value):
    if not value:
        return 0.0
    cleaned = value.replace(",", "").strip()
    try:
        return float(cleaned)
    except ValueError:
        return 0.0
